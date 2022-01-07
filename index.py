# -*- coding: utf8 -*-
import json
from cbnew_pre import main


def main_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    # print("Received context: " + str(context))
    # print("Hello world")
    # return("Hello World")
    main()
