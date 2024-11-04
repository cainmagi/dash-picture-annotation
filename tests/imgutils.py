# -*- coding: UTF-8 -*-
"""
Utilities
=========
@ Dash Picture Annotation - Tests

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
Extra functionalities used for enhancing the tests.
"""

import os
import io
import base64

from typing import Union, Optional

try:
    from typing import Sequence
    from typing import Tuple
except ImportError:
    from collections.abc import Sequence
    from builtins import tuple as Tuple

from typing_extensions import Literal

from PIL import Image, ImageOps, ImageChops
import numpy as np
from skimage.metrics import structural_similarity as ssim


__all__ = (
    "image_rgba_to_rgb",
    "remove_image_margin",
    "decode_base64_image",
    "compare_images",
    "compare_images_with_alpha",
    "ImageLoader",
)


def image_rgba_to_rgb(img: Image.Image, background: str = "black") -> Image.Image:
    """Convert an RGBA image to an RGB image by adding a background color."""
    return Image.alpha_composite(Image.new("RGBA", img.size, background), img).convert(
        "RGB"
    )


def remove_image_margin(img: Image.Image) -> Image.Image:
    """Remove the margin of an image."""
    if img.mode.casefold() == "rgba":
        bounding_box = img.getbbox()
        if bounding_box:
            img = img.crop(bounding_box)
        img_a = ImageOps.invert(image_rgba_to_rgb(img, "white"))
        img_b = image_rgba_to_rgb(img, "black")
    else:
        img_b = img.convert("RGB")
        img_a = ImageOps.invert(img_b)
    bounding_box = ImageChops.lighter(
        ImageChops.subtract(
            img_a, Image.new("RGB", img_a.size, img_a.getpixel((0, 0))), 1.0, -100
        ),
        ImageChops.subtract(
            img_b, Image.new("RGB", img_b.size, img_b.getpixel((0, 0))), 1.0, -100
        ),
    ).getbbox()
    if bounding_box:
        img = img.crop(bounding_box)
    return img


def decode_base64_image(text: str, use_rgba: bool = False) -> Image.Image:
    """Decode the base64 encoded png image to the correct image."""
    img = Image.open(
        io.BytesIO(base64.b64decode(text[len("data:image/png;base64,") :])),
        formats=("png", "webp", "jpeg"),
    )
    img.load()
    img = remove_image_margin(img)
    if img.mode.casefold() == "rgba":
        if not use_rgba:
            img = image_rgba_to_rgb(img, "white")
    if use_rgba:
        if img.mode.casefold() != "rgba":
            img = img.convert("RGBA")
    else:
        img = img.convert("RGB")
    return img


def compare_images(
    image: Image.Image, ref: Image.Image, size: Optional[Tuple[int, int]] = None
) -> float:
    """Compare two images, calculate the similarity bettween then, assuming that the
    images do not contain the alpha channels.

    Arguments
    ---------
    image: `Image`
        The image to be checked.

    ref: `Image`
        The reference image to be used for comparison. Note that the reference image
        will be used for specifying the data range.

    size: `(int, int) | None`
        The resize target applied to the images before the comparison. If not
        specified, will resize the width to be 100.
    """
    if size is None:
        size = (100, max(1, int(round(ref.size[1] * 100 / ref.size[0]))))
    image_data = np.asarray(
        image.convert(mode="RGB").resize(size, Image.Resampling.LANCZOS)
    )
    ref_data = np.asarray(
        ref.convert(mode="RGB").resize(size, Image.Resampling.LANCZOS)
    )
    return float(
        ssim(
            image_data,
            ref_data,
            data_range=ref_data.max() - ref_data.min(),
            channel_axis=2,
        )
    )


def compare_images_with_alpha(
    image: Image.Image,
    ref: Image.Image,
    size: Optional[Tuple[int, int]] = None,
    fine_mode: bool = False,
) -> float:
    """Compare two images, calculate the similarity bettween them, and weight the
    similarity by the alpha channel.

    Arguments
    ---------
    image: `Image`
        The image to be checked.

    ref: `Image`
        The reference image to be used for comparison. Note that the reference image
        will be used for specifying the data range and the alpha channel weight.

    size: `(int, int) | None`
        The resize target applied to the images before the comparison. If not
        specified, will resize the width to be 100.

    fine_mode: `bool`
        A flag. Whether to turn on the fine mode. If specified, will not use the
        binary alpha channel to select and calculate the averaged ssim, but use the
        alpha channel as the weight of the ssim. This configuration will make the
        weight of ssim values more fine-grained.
    """
    if size is None:
        size = (100, max(1, int(round(ref.size[1] * 100 / ref.size[0]))))
    image = image.convert(mode="RGBA").resize(size, Image.Resampling.LANCZOS)
    ref = ref.convert(mode="RGBA").resize(size, Image.Resampling.LANCZOS)

    ref_data = np.asarray(image_rgba_to_rgb(ref, "white"))
    _, ssim_img_white = ssim(
        np.asarray(image_rgba_to_rgb(image, "white")),
        ref_data,
        data_range=ref_data.max() - ref_data.min(),
        channel_axis=2,
        full=True,
    )

    ref_data = np.asarray(image_rgba_to_rgb(ref, "black"))
    _, ssim_img_black = ssim(
        np.asarray(image_rgba_to_rgb(image, "black")),
        ref_data,
        data_range=ref_data.max() - ref_data.min(),
        channel_axis=2,
        full=True,
    )

    val_ssim = np.asarray(np.minimum(ssim_img_black, ssim_img_white))
    if fine_mode:
        mask_alpha = np.asarray(ref.split()[-1])
        mask_alpha = mask_alpha / max(1.0, np.amax(mask_alpha))
        weight = np.sum(mask_alpha) * val_ssim.shape[-1]
        if weight < 1e-3:
            return 1.0
        else:
            return float(
                np.sum(
                    np.reshape(val_ssim, (-1, val_ssim.shape[-1]))
                    * np.expand_dims(mask_alpha.flatten(), axis=-1)
                )
                / weight
            )
    else:
        mask_alpha = np.asarray(ref.split()[-1]) < 100
        return float(
            np.mean(
                np.reshape(val_ssim, (-1, val_ssim.shape[-1]))[mask_alpha.flatten(), :]
            )
        )


class ImageLoader:
    """Loader for images.

    This object is used for dynamically loading images from a specific folder during
    the test.
    """

    def __init__(
        self,
        root: str,
        mode: Literal["RGB", "RGBA"] = "RGBA",
        ext_list: Union[Sequence[str], str] = "webp",
    ) -> None:
        """Initialization.

        Arguments
        ---------
        root: `str`
            The root path of the images to be read.

        mode: `"RGB" | "RGBA"`
            The mode used for saving images.

        ext_list: `[str] | str`
            The list of file name extensions to be searched.
        """
        self.root = str(root)
        if not os.path.isdir(self.root):
            raise FileNotFoundError(
                'The argument "root" specifies a path that is not a folder.'
            )
        self.mode = mode
        self.ext_list = (ext_list,) if isinstance(ext_list, str) else tuple(ext_list)

    def __normalize_path(self, file_path: str) -> str:
        """Normalize the path of a file for ensuring that the path refers to an
        existing file.

        If no valid file can be detected, will return the input `file_path` directly.
        """
        if os.path.isfile(file_path):
            return file_path
        for ext in self.ext_list:
            _file_path = "{0}.{1}".format(file_path, ext)
            if os.path.isfile(_file_path):
                return _file_path
        _file_path = os.path.splitext(file_path)[0]
        if os.path.isfile(_file_path):
            return _file_path
        for ext in self.ext_list:
            _file_path_v2 = "{0}.{1}".format(_file_path, ext)
            if os.path.isfile(_file_path_v2):
                return _file_path_v2
        return file_path

    def __getitem__(self, file_name: str) -> Image.Image:
        """Load a image by calling the `__getitem__` method."""
        file_path = self.__normalize_path(os.path.join(self.root, file_name))
        with open(file_path, "rb") as fobj:
            img = Image.open(fobj, formats=self.ext_list)
            img.load()
        return img

    def __setitem__(self, file_name: str, img: Image.Image) -> None:
        """Save the image as a reference image in the root folder."""
        file_path = os.path.join(self.root, file_name)
        if not os.path.isfile(file_path):
            file_path_base, ext = os.path.splitext(file_name)
            if ext.casefold().strip().strip(".") not in self.ext_list:
                ext = ".{0}".format(self.ext_list[0])
            file_path = file_path_base + ext
        size = (100, max(1, int(round(img.size[1] * 100 / img.size[0]))))
        ext = os.path.splitext(file_path)[-1].casefold().strip().strip(".")
        img.convert(mode=self.mode).resize(size, Image.Resampling.LANCZOS).save(
            os.path.join("tests", "assets", file_path),
            format=ext if ext in self.ext_list else "webp",
            lossless=True,
            exact=True,
        )
