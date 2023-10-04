#!/usr/bin/env python3
import os

import aws_cdk as cdk

from src.experimento1_stack import Experimento1Stack


app = cdk.App()
Experimento1Stack(app, "Experimento1Stack")

app.synth()
