# Copyright 2020 Farzad Senart and Lionel Suss. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict, Final, List

from . import Tag

_NAMESPACE = "AWS::Inspector"

class AssessmentTarget:
    """Documentation: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html"""

    Arn: Final[str]

    Ref: Final[str]
    def __init__(
        self,
        *,
        AssessmentTargetName: str = ...,
        DeletionPolicy: str = ...,
        DependsOn: List[Any] = ...,
        ResourceGroupArn: str = ...,
        UpdateReplacePolicy: str = ...
    ): ...

class AssessmentTemplate:
    """Documentation: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html"""

    Arn: Final[str]

    Ref: Final[str]
    def __init__(
        self,
        *,
        AssessmentTargetArn: str,
        DurationInSeconds: int,
        RulesPackageArns: List[str],
        AssessmentTemplateName: str = ...,
        DeletionPolicy: str = ...,
        DependsOn: List[Any] = ...,
        UpdateReplacePolicy: str = ...,
        UserAttributesForFindings: List["Tag"] = ...
    ): ...

class ResourceGroup:
    """Documentation: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html"""

    Arn: Final[str]

    Ref: Final[str]
    def __init__(
        self,
        *,
        ResourceGroupTags: List["Tag"],
        DeletionPolicy: str = ...,
        DependsOn: List[Any] = ...,
        UpdateReplacePolicy: str = ...
    ): ...
