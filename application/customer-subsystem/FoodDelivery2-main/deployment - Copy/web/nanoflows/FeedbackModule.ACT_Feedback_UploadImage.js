import { addEnumerations, t } from "mendix";

export const ACT_Feedback_UploadImage = {
  "name": "FeedbackModule.ACT_Feedback_UploadImage",
  "instructions": [
    {
      "type": "setVariable",
      "label": "36831bdc-f377-407f-a3bf-996db2620ac7",
      "value": {
        "type": "literal",
        "value": ".gif,.png,.jpg,.jpeg"
      },
      "outputVar": "mimeTypes",
      "outputKind": "primitive"
    },
    {
      "type": "setVariable",
      "label": "ce306032-2aae-42c3-885e-6e368f57a088",
      "value": {
        "type": "literalNumeric",
        "value": "5"
      },
      "outputVar": "fileUploadSize",
      "outputKind": "primitive"
    },
    {
      "type": "javaScriptActionCall",
      "label": "64ea4562-0d1a-484b-878f-557a761d4d1b",
      "action": () => require("C:/Users/Korisnik/Mendix/FoodDelivery2-main/javascriptsource/feedbackmodule/actions/JS_UploadAndConvertToFileBlobURL").JS_UploadAndConvertToFileBlobURL,
      "outputVar": "fileBlobURL",
      "parameters": [
        {
          "kind": "primitive",
          "value": {
            "type": "variable",
            "variable": "mimeTypes"
          }
        },
        {
          "kind": "primitive",
          "value": {
            "type": "variable",
            "variable": "fileUploadSize"
          }
        }
      ]
    },
    {
      "type": "switch",
      "label": "393def4e-7bfc-4305-b613-bf897a304555",
      "condition": {
        "type": "function",
        "name": "!=",
        "parameters": [
          {
            "type": "variable",
            "variable": "fileBlobURL"
          },
          {
            "type": "literal",
            "value": "uploadCancelled"
          }
        ]
      },
      "targets": {
        "true": "9d45439d-3e20-4de3-b319-27e239f165f8",
        "false": "66db9f5d-1219-4a12-bee1-2f153b051977"
      }
    },
    {
      "type": "return",
      "label": "66db9f5d-1219-4a12-bee1-2f153b051977",
      "result": {
        "type": "literal",
        "value": null
      },
      "resultKind": "primitive"
    },
    {
      "type": "switch",
      "label": "9d45439d-3e20-4de3-b319-27e239f165f8",
      "condition": {
        "type": "function",
        "name": "!=",
        "parameters": [
          {
            "type": "variable",
            "variable": "fileBlobURL"
          },
          {
            "type": "literal",
            "value": null
          }
        ]
      },
      "targets": {
        "false": "7ca45ffe-edb5-430f-b1dd-1ff30ef4987e",
        "true": "98b70e00-4746-4105-87e8-aa1cb87bc13c"
      }
    },
    {
      "type": "switch",
      "label": "98b70e00-4746-4105-87e8-aa1cb87bc13c",
      "condition": {
        "type": "function",
        "name": "!=",
        "parameters": [
          {
            "type": "variable",
            "variable": "fileBlobURL"
          },
          {
            "type": "literal",
            "value": "fileSizeNotAccepted"
          }
        ]
      },
      "targets": {
        "true": "327e87e4-1157-40e8-bbd6-176f0b491653",
        "false": "b02539d5-09a5-4461-b950-2358a0e5f4ea"
      }
    },
    {
      "type": "showMessage",
      "label": "b02539d5-09a5-4461-b950-2358a0e5f4ea",
      "messageType": "error",
      "message": t([
        {
          "type": "literal",
          "value": "Maximum image size allowed is 5MB."
        }
      ]),
      "blocking": true
    },
    {
      "type": "return",
      "label": "35129755-2325-4321-8aa1-063fe6961554",
      "result": {
        "type": "literal",
        "value": null
      },
      "resultKind": "primitive"
    },
    {
      "type": "switch",
      "label": "327e87e4-1157-40e8-bbd6-176f0b491653",
      "condition": {
        "type": "function",
        "name": "!=",
        "parameters": [
          {
            "type": "variable",
            "variable": "fileBlobURL"
          },
          {
            "type": "literal",
            "value": "fileTypeNotAccepted"
          }
        ]
      },
      "targets": {
        "false": "86542016-556c-4ba3-853e-981a54baebb9",
        "true": "be05da77-fa06-4c7c-a8c8-1c229ae5de08"
      }
    },
    {
      "type": "closeForm",
      "label": "be05da77-fa06-4c7c-a8c8-1c229ae5de08"
    },
    {
      "type": "javaScriptActionCall",
      "label": "aefaf686-9694-4219-998c-241f884f910e",
      "action": () => require("C:/Users/Korisnik/Mendix/FoodDelivery2-main/javascriptsource/feedbackmodule/actions/JS_ToggleFeedbackAnnotateWidget").JS_ToggleFeedbackAnnotateWidget,
      "outputVar": "base64ImageFromWidget",
      "parameters": [
        {
          "kind": "primitive",
          "value": {
            "type": "variable",
            "variable": "fileBlobURL"
          }
        }
      ]
    },
    {
      "type": "changeObject",
      "label": "68ddebc3-9a15-44b5-9136-f0073c0610f9",
      "inputVar": "Feedback",
      "member": "ImageB64",
      "value": {
        "type": "variable",
        "variable": "base64ImageFromWidget"
      }
    },
    {
      "type": "commitObjects",
      "operationId": "+vYLvw2DeVytow+5wSbYGw",
      "inputVar": "Feedback"
    },
    {
      "type": "openForm",
      "label": "72a47953-0896-4727-9e96-3952b130fce9",
      "path": "FeedbackModule/ShareFeedback.page.xml",
      "params": {
        "name": "FeedbackModule/ShareFeedback.page.xml",
        "location": "modal",
        "resizable": true
      }
    },
    {
      "type": "javaScriptActionCall",
      "label": "1d5ef0d4-177c-4a2e-a64e-455950cbd5c2",
      "action": () => require("C:/Users/Korisnik/Mendix/FoodDelivery2-main/javascriptsource/feedbackmodule/actions/JS_SetFeedbackStorageObject").JS_SetFeedbackStorageObject,
      "parameters": [
        {
          "kind": "primitive",
          "value": {
            "type": "constant",
            "name": "FeedbackModule.LocalStorageKey"
          }
        },
        {
          "kind": "object",
          "value": {
            "type": "variable",
            "variable": "Feedback"
          }
        }
      ]
    },
    {
      "type": "javaScriptActionCall",
      "label": "a4ce3585-da9d-4265-8dc4-3057fa99774a",
      "action": () => require("C:/Users/Korisnik/Mendix/FoodDelivery2-main/javascriptsource/feedbackmodule/actions/JS_RevokeUploadedFileFromMemory").JS_RevokeUploadedFileFromMemory,
      "parameters": [
        {
          "kind": "primitive",
          "value": {
            "type": "variable",
            "variable": "fileBlobURL"
          }
        }
      ]
    },
    {
      "type": "return",
      "label": "a2b4b8b7-8024-4d28-868d-1b506d219771",
      "result": {
        "type": "literal",
        "value": null
      },
      "resultKind": "primitive"
    },
    {
      "type": "showMessage",
      "label": "86542016-556c-4ba3-853e-981a54baebb9",
      "messageType": "error",
      "message": t([
        {
          "type": "literal",
          "value": "Only images with format of .gif .jpg .jpeg .png are allowed"
        }
      ]),
      "blocking": true
    },
    {
      "type": "return",
      "label": "7589b73a-f6b2-41ab-a46b-107b4b18d5bc",
      "result": {
        "type": "literal",
        "value": null
      },
      "resultKind": "primitive"
    },
    {
      "type": "showMessage",
      "label": "7ca45ffe-edb5-430f-b1dd-1ff30ef4987e",
      "messageType": "error",
      "message": t([
        {
          "type": "literal",
          "value": "Upload failed, please try again."
        }
      ]),
      "blocking": true
    },
    {
      "type": "return",
      "label": "8d2a153c-6ee9-4bba-a713-71333f81187d",
      "result": {
        "type": "literal",
        "value": null
      },
      "resultKind": "primitive"
    }
  ]
};
