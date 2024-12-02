import type {SidebarsConfig} from "@docusaurus/plugin-content-docs";

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  // tutorial: [{type: 'autogenerated', dirName: '.'}],

  // But you can create a sidebar manually
  tutorial: [
    "introduction",
    "tutorial/install",
    {
      type: "category",
      label: "Usages",
      collapsed: false,
      link: {
        type: "generated-index",
        title: "How to use DashPictureAnnotation",
        slug: "/category/usages",
        description:
          "Simple guides for showing the basic usages of this component.",
      },
      items: [
        "tutorial/usages/data",
        "tutorial/usages/colors",
        "tutorial/usages/image",
      ],
    },
    {
      type: "category",
      label: "Examples",
      collapsed: true,
      link: {
        type: "generated-index",
        title: "Examples",
        slug: "/category/examples",
        description: "Explanations of the example codes.",
      },
      items: [
        "tutorial/examples/minimal",
        "tutorial/examples/states",
        "tutorial/examples/size-control",
        "tutorial/examples/options",
        "tutorial/examples/colors",
      ],
    },
    "license",
  ],

  apis: [
    "api-overview",
    {
      type: "category",
      label: "typehints",
      collapsed: true,
      link: {
        type: "doc",
        id: "apis/typehints/index",
      },
      items: [
        "apis/typehints/AnnoMark",
        "apis/typehints/AnnoItem",
        "apis/typehints/Annotations",
        "apis/typehints/AnnoStyle",
        "apis/typehints/DashSelectOptionItem",
        "apis/typehints/Size",
        "apis/typehints/NSAnnoItem",
        "apis/typehints/NSAnnotations",
        "apis/typehints/is_sequence_of",
        "apis/typehints/is_anno_mark",
        "apis/typehints/is_anno_item",
        "apis/typehints/is_annotations",
        "apis/typehints/is_dash_select_option_item",
      ],
    },
    {
      type: "category",
      label: "utilities",
      collapsed: true,
      link: {
        type: "doc",
        id: "apis/utilities/index",
      },
      items: [
        "apis/utilities/get_data_item",
        "apis/utilities/get_data_item_with_default",
        "apis/utilities/get_data_items",
        "apis/utilities/get_data_items_by_regex",
        "apis/utilities/get_all_ids",
        "apis/utilities/get_all_comments",
        "apis/utilities/compare_anno_marks",
        "apis/utilities/sanitize_data_item",
        "apis/utilities/sanitize_data",
      ],
    },
    "apis/DashPictureAnnotation",
  ],
};

export default sidebars;