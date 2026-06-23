import { addEnumerations, t } from "mendix";
import { SUB_Feedback_ResetLocalStorage } from "./FeedbackModule.SUB_Feedback_ResetLocalStorage.js";

export const ACT_SubmitFeedback = {
  "name": "FeedbackModule.ACT_SubmitFeedback",
  "instructions": [
    {
      "type": "microflowCall",
      "label": "7564f11c-cb0c-41d2-a4a3-ccfe7ada23e8",
      "operationId": "XYFaERXHGVmxSIMs2fY56Q",
      "parameters": [
        {
          "name": "Feedback",
          "value": {
            "type": "variable",
            "variable": "Feedback"
          },
          "kind": "object"
        }
      ],
      "outputVar": "isValid"
    },
    {
      "type": "switch",
      "label": "dd3cc359-178d-450c-bc2c-227740ae5d0a",
      "condition": {
        "type": "variable",
        "variable": "isValid"
      },
      "targets": {
        "true": "02714b53-6842-4cf0-b7a7-f448f39735f2",
        "false": "7d984602-1675-4806-bacd-184db96c4365"
      }
    },
    {
      "type": "return",
      "label": "7d984602-1675-4806-bacd-184db96c4365",
      "result": {
        "type": "literal",
        "value": null
      },
      "resultKind": "primitive"
    },
    {
      "type": "microflowCall",
      "label": "02714b53-6842-4cf0-b7a7-f448f39735f2",
      "operationId": "F78r2LFOCFSJT0k3EV0Pzg",
      "parameters": [
        {
          "name": "Feedback",
          "value": {
            "type": "variable",
            "variable": "Feedback"
          },
          "kind": "object"
        }
      ],
      "outputVar": "ResponseHelper"
    },
    {
      "type": "closeForm",
      "label": "4965bb03-45ce-44a1-a5dc-d77800aac6de",
      "numberOfPagesToClose": {
        "type": "literalNumeric",
        "value": "1"
      }
    },
    {
      "type": "switch",
      "label": "f527651e-3ddf-4224-a0ea-460715172948",
      "condition": {
        "type": "function",
        "name": "!=",
        "parameters": [
          {
            "type": "variable",
            "variable": "ResponseHelper"
          },
          {
            "type": "literal",
            "value": null
          }
        ]
      },
      "targets": {
        "true": "b0a561dd-615b-4555-9a89-ed4125943a79",
        "false": "436e22a2-0914-4abb-b5ed-0b4e003791fd"
      }
    },
    {
      "type": "jump",
      "label": "436e22a2-0914-4abb-b5ed-0b4e003791fd",
      "target": "b2ceb294-a5ad-4f79-9c65-d4270e3cb861"
    },
    {
      "type": "openForm",
      "label": "b2ceb294-a5ad-4f79-9c65-d4270e3cb861",
      "path": "FeedbackModule/PopupFailure.page.xml",
      "params": {
        "name": "FeedbackModule/PopupFailure.page.xml",
        "location": "modal",
        "resizable": false
      }
    },
    {
      "type": "return",
      "label": "fce2589c-a010-400c-8a99-0359166a1fd8",
      "result": {
        "type": "literal",
        "value": null
      },
      "resultKind": "primitive"
    },
    {
      "type": "openForm",
      "label": "b0a561dd-615b-4555-9a89-ed4125943a79",
      "path": "FeedbackModule/PopupSuccess.page.xml",
      "params": {
        "name": "FeedbackModule/PopupSuccess.page.xml",
        "location": "modal",
        "resizable": false
      },
      "inputArgs": {
        "$Response": {
          "type": "variable",
          "variable": "ResponseHelper"
        }
      }
    },
    {
      "type": "nanoflowCall",
      "label": "36dd775e-1ca6-48d4-9c28-387bd674bb37",
      "flow": () => SUB_Feedback_ResetLocalStorage,
      "parameters": [
        {
          "name": "Feedback",
          "value": {
            "type": "variable",
            "variable": "Feedback"
          },
          "kind": "object"
        }
      ]
    },
    {
      "type": "return",
      "label": "675a3b07-d601-48be-9222-6307b3119dbf",
      "result": {
        "type": "literal",
        "value": null
      },
      "resultKind": "primitive"
    }
  ]
};
