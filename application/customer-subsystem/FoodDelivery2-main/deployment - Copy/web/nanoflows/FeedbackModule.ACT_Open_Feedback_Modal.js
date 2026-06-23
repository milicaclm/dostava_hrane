import { addEnumerations, t } from "mendix";

export const ACT_Open_Feedback_Modal = {
  "name": "FeedbackModule.ACT_Open_Feedback_Modal",
  "instructions": [
    {
      "type": "openForm",
      "label": "82e83e5c-cc5f-4673-8f36-9404a9019c7a",
      "path": "FeedbackModule/ShareFeedback.page.xml",
      "params": {
        "name": "FeedbackModule/ShareFeedback.page.xml",
        "location": "modal",
        "resizable": true
      }
    },
    {
      "type": "return",
      "label": "f726a77f-b8cb-4bba-b14a-ca08d103fb1d",
      "result": {
        "type": "literal",
        "value": null
      },
      "resultKind": "primitive"
    }
  ]
};
