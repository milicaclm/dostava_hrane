import { addEnumerations, t } from "mendix";

export const ACT_Feedback_TriggerScreenshotMode = {
  "name": "FeedbackModule.ACT_Feedback_TriggerScreenshotMode",
  "instructions": [
    {
      "type": "closeForm",
      "label": "9dddd184-f047-48b0-a7ba-87e73872e35d"
    },
    {
      "type": "javaScriptActionCall",
      "label": "92d604b1-9ae2-45fc-a3e5-9a99cfad7ed5",
      "action": () => require("C:/Users/Korisnik/Mendix/FoodDelivery2-main/javascriptsource/feedbackmodule/actions/JS_ToggleFeedbackScreenshotWidget").JS_ToggleFeedbackScreenshotWidget,
      "outputVar": "base64FromWidget",
      "parameters": []
    },
    {
      "type": "switch",
      "label": "6348015f-f760-424c-8008-c02a6b1b870d",
      "condition": {
        "type": "function",
        "name": "!=",
        "parameters": [
          {
            "type": "variable",
            "variable": "base64FromWidget"
          },
          {
            "type": "literal",
            "value": "uploadCancelled"
          }
        ]
      },
      "targets": {
        "true": "bdc678b6-d529-4afc-b897-212b84ab0f5d",
        "false": "b3935190-9b62-4fed-ad83-b25057375a4a"
      }
    },
    {
      "type": "jump",
      "label": "b3935190-9b62-4fed-ad83-b25057375a4a",
      "target": "c877f0c7-8eab-498f-b4fb-9832a1d1c65e"
    },
    {
      "type": "jump",
      "label": "c877f0c7-8eab-498f-b4fb-9832a1d1c65e",
      "target": "cabefb3c-e657-495f-9d00-11920eff022c"
    },
    {
      "type": "jump",
      "label": "cabefb3c-e657-495f-9d00-11920eff022c",
      "target": "06de7688-21d8-4eca-8296-fb0a4e0c9a66"
    },
    {
      "type": "openForm",
      "label": "06de7688-21d8-4eca-8296-fb0a4e0c9a66",
      "path": "FeedbackModule/ShareFeedback.page.xml",
      "params": {
        "name": "FeedbackModule/ShareFeedback.page.xml",
        "location": "modal",
        "resizable": true
      }
    },
    {
      "type": "return",
      "label": "f8ef480a-ac5b-429e-9a45-83274499ebcf",
      "result": {
        "type": "literal",
        "value": null
      },
      "resultKind": "primitive"
    },
    {
      "type": "switch",
      "label": "bdc678b6-d529-4afc-b897-212b84ab0f5d",
      "condition": {
        "type": "function",
        "name": "!=",
        "parameters": [
          {
            "type": "variable",
            "variable": "base64FromWidget"
          },
          {
            "type": "literal",
            "value": null
          }
        ]
      },
      "targets": {
        "true": "aac9b983-d86e-48f5-8736-5970e49a065e",
        "false": "53357d12-ce73-438c-9016-8cc7bec52a51"
      }
    },
    {
      "type": "return",
      "label": "53357d12-ce73-438c-9016-8cc7bec52a51",
      "result": {
        "type": "literal",
        "value": null
      },
      "resultKind": "primitive"
    },
    {
      "type": "javaScriptActionCall",
      "label": "aac9b983-d86e-48f5-8736-5970e49a065e",
      "action": () => require("C:/Users/Korisnik/Mendix/FoodDelivery2-main/javascriptsource/feedbackmodule/actions/JS_isStrictMode").JS_isStrictMode,
      "outputVar": "isStrictMode",
      "parameters": []
    },
    {
      "type": "switch",
      "label": "798cd39a-4c7a-4ab5-9842-4417ad8c7d6a",
      "condition": {
        "type": "function",
        "name": "=",
        "parameters": [
          {
            "type": "variable",
            "variable": "isStrictMode"
          },
          {
            "type": "literal",
            "value": false
          }
        ]
      },
      "targets": {
        "true": "2e3018e2-29fe-462f-984f-aad015659326",
        "false": "83fef770-06b3-429c-b3cc-83e1e8be43f9"
      }
    },
    {
      "type": "jump",
      "label": "83fef770-06b3-429c-b3cc-83e1e8be43f9",
      "target": "6bcdd358-e8cb-43ee-bd4e-fdfaa63c34b2"
    },
    {
      "type": "javaScriptActionCall",
      "label": "6bcdd358-e8cb-43ee-bd4e-fdfaa63c34b2",
      "action": () => require("C:/Users/Korisnik/Mendix/FoodDelivery2-main/javascriptsource/feedbackmodule/actions/JS_SetSingleLocalStorageObjectItem").JS_SetSingleLocalStorageObjectItem,
      "parameters": [
        {
          "kind": "primitive",
          "value": {
            "type": "constant",
            "name": "FeedbackModule.LocalStorageKey"
          }
        },
        {
          "kind": "primitive",
          "value": {
            "type": "variable",
            "variable": "base64FromWidget"
          }
        }
      ]
    },
    {
      "type": "jump",
      "label": "fbbcc98f-0730-4749-8baf-4d2aca6d45d0",
      "target": "cabefb3c-e657-495f-9d00-11920eff022c"
    },
    {
      "type": "jump",
      "label": "cabefb3c-e657-495f-9d00-11920eff022c",
      "target": "06de7688-21d8-4eca-8296-fb0a4e0c9a66"
    },
    {
      "type": "changeObject",
      "label": "2e3018e2-29fe-462f-984f-aad015659326",
      "inputVar": "Feedback",
      "member": "ImageB64",
      "value": {
        "type": "variable",
        "variable": "base64FromWidget"
      }
    },
    {
      "type": "commitObjects",
      "operationId": "a4JIIGAtsVSQb2qRLmjfpA",
      "inputVar": "Feedback"
    },
    {
      "type": "jump",
      "label": "cabefb3c-e657-495f-9d00-11920eff022c",
      "target": "06de7688-21d8-4eca-8296-fb0a4e0c9a66"
    }
  ]
};
