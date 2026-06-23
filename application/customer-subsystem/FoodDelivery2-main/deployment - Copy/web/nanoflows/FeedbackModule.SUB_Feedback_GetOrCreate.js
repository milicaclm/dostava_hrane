import { addEnumerations, t } from "mendix";
import { Get_And_Set_Feedback_NPE } from "./FeedbackModule.Get_And_Set_Feedback_NPE.js";

export const SUB_Feedback_GetOrCreate = {
  "name": "FeedbackModule.SUB_Feedback_GetOrCreate",
  "instructions": [
    {
      "type": "javaScriptActionCall",
      "label": "14f94073-ab60-4a9c-a33f-490743640a04",
      "action": () => require("C:/Users/Korisnik/Mendix/FoodDelivery2-main/javascriptsource/feedbackmodule/actions/JS_isStrictMode").JS_isStrictMode,
      "outputVar": "isStrictMode",
      "parameters": []
    },
    {
      "type": "switch",
      "label": "ed9d4752-36c3-4f02-af79-98c4f2d6872e",
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
        "false": "377de816-4910-4ea5-a3ec-162f3908c4f9",
        "true": "82efdf51-9755-4f03-b1dc-8ef36d314661"
      }
    },
    {
      "type": "tryCatch",
      "label": "82efdf51-9755-4f03-b1dc-8ef36d314661",
      "catchTarget": "6a45f39e-5d70-48d0-b69a-f5d4b8fda12e",
      "body": [
        {
          "type": "javaScriptActionCall",
          "action": () => require("C:/Users/Korisnik/Mendix/FoodDelivery2-main/javascriptsource/feedbackmodule/actions/JS_GetFeedbackStorageObject").JS_GetFeedbackStorageObject,
          "outputVar": "LocalFeedback",
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
                "type": "literal",
                "value": "FeedbackModule.Feedback"
              }
            }
          ]
        },
        {
          "type": "return",
          "result": {
            "type": "literal",
            "value": true
          },
          "resultKind": "primitive"
        }
      ]
    },
    {
      "type": "switch",
      "label": "81aa943d-2c9d-4097-83c0-18da6955c2ba",
      "condition": {
        "type": "function",
        "name": "!=",
        "parameters": [
          {
            "type": "variable",
            "variable": "LocalFeedback"
          },
          {
            "type": "literal",
            "value": null
          }
        ]
      },
      "targets": {
        "false": "476a9b52-e565-4f99-a6af-65afb06eeedb",
        "true": "d64a6f85-d77c-4493-99ba-3d038b432195"
      }
    },
    {
      "type": "return",
      "label": "d64a6f85-d77c-4493-99ba-3d038b432195",
      "result": {
        "type": "variable",
        "variable": "LocalFeedback"
      },
      "resultKind": "object"
    },
    {
      "type": "jump",
      "label": "476a9b52-e565-4f99-a6af-65afb06eeedb",
      "target": "56ff7a1e-738a-4403-9b6b-de2919999239"
    },
    {
      "type": "createObject",
      "label": "56ff7a1e-738a-4403-9b6b-de2919999239",
      "objectType": "FeedbackModule.Feedback",
      "outputVar": "NewFeedback"
    },
    {
      "type": "return",
      "label": "3e2dfb64-d55a-448e-a4b0-a7e4973e988a",
      "result": {
        "type": "variable",
        "variable": "NewFeedback"
      },
      "resultKind": "object"
    },
    {
      "type": "jump",
      "label": "6a45f39e-5d70-48d0-b69a-f5d4b8fda12e",
      "target": "476a9b52-e565-4f99-a6af-65afb06eeedb"
    },
    {
      "type": "jump",
      "label": "476a9b52-e565-4f99-a6af-65afb06eeedb",
      "target": "56ff7a1e-738a-4403-9b6b-de2919999239"
    },
    {
      "type": "jump",
      "label": "377de816-4910-4ea5-a3ec-162f3908c4f9",
      "target": "3c73f11f-9698-4f7d-bfa5-d207e6c982d7"
    },
    {
      "type": "nanoflowCall",
      "label": "3c73f11f-9698-4f7d-bfa5-d207e6c982d7",
      "flow": () => Get_And_Set_Feedback_NPE,
      "parameters": [],
      "outputVar": "StrictModeFeedback"
    },
    {
      "type": "return",
      "label": "2c32cb36-135a-464a-8feb-487aaf9ad8db",
      "result": {
        "type": "variable",
        "variable": "StrictModeFeedback"
      },
      "resultKind": "object"
    }
  ]
};
