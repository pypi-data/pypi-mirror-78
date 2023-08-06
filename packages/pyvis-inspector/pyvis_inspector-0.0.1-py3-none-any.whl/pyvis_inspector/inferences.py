
import requests as res
import json
from . import tokens


# TODO: add class doc strings


class Inferences:

    def __init__(self):
        self.path = "http://poc.maximovisualinspection.com/visual-inspection-ny/api/"


class Inspection(Inferences):

    def inspect(self, model_id: str, imageUrl: str, **kwargs) -> dict:
        """
        Checks image against a Visual Inspector Deployed Model

        :param model_id: ID of deployed model
        :param imageUrl: URL image path to run check against.

        containHeatMap: (optional) Flag parameter to request inclusion of the heat map in classification results.
        This parameter is only applicable on classification models and is ignored on on all model types.
        Possible values are "true" to include the heat map, or "false" to exclude the heat map.
        The default value is "false" if the parameter is not provided.

        containRle: (optional) Flag parameter to request inclusion of the compressed RLE string in object detection
        segmentation results. This parameter is only applicable on object detection models that can provide instance
        segmentation results. It is ignored on on all model types. Possible values are "true" to include the compressed
        RLE string, or "false" to exclude it.>br> The default value is "false" if the parameter is not provided.

        containPolygon: (optional) Flag parameter to request inclusion of the polygon boundary information in object
        detection segmentaion results. This parameter is only applicable on object detection models that can provide
        instance segmentation results. It is ignored on on all model types. Possible values are "true" to include the
        polygon information, or "false" to exclude it. The default value is "true" if the parameter is not provided.

        confthre: (optional) Parameter to specify the confidence threshold to use when providing results. This parameter
        applies to both classification and object detection models. It is a floating point value that specifies the
        threshold at which possible matches are to be excluded from the result set. A value of 0.5 will exclude possible
        matches with a confidence score below 50%. Possible values range from 0.0 to 0.9. The default value is 0.0 if
        this parameter is not specified.

        clsnum: (optional) This parameter is used to identify how many different possible matches are included in the
        results. For classification, this means that if there are multiple possible matches with a confidence score
        above the confthre value, up to the indicated value matches are included in the result. Values are integer
        values where 0 is the default (which means to include all possible matches in the results).

        waitForResults: (optional) This parameter is used for video inferencing. By default, video inference results are
        reported asynchronously -- meaning that the call to do the inference will return while processing continues on
        the video. Inference results are available via the /inferences endpoint. If this parameter is passed with a
        value of "true" (case is ignored), the endpoint will not return until the video has completed processing. The
        JSON results will be returned at that time. Note that the JSON results will also be available via the
        VideoInferences class.

        genCaption: (optional) This parameter is used for video inferencing. It controls whether or not a "captioned"
        video should be generated and stored with the inferencing results. The default varies by the detection being
        done. For Action Detection, the default is to generate a captioned video. For Object Detection, the default
        is to NOT generate a captioned video. The captioned video is accessible via the VideoInferences class.

        :return: Dictionary of model results
        """

        message = self.path + f"dlapis/{model_id}?imageUrl={imageUrl}"

        for key, value in kwargs.items():
            message += f'&{key}={value}'

        return json.loads(res.get(message).text)

    def inspect_up(self, model_id: str, image_path: str, **kwargs) -> dict:
        """
        Checks image against a Visual Inspector Deployed Model

        :param model_id: ID of deployed model
        :param image_path: Local image path to run check against.

        containHeatMap: (optional) Flag parameter to request inclusion of the heat map in classification results.
        This parameter is only applicable on classification models and is ignored on on all model types.
        Possible values are "true" to include the heat map, or "false" to exclude the heat map.
        The default value is "false" if the parameter is not provided.

        containRle: (optional) Flag parameter to request inclusion of the compressed RLE string in object detection
        segmentation results. This parameter is only applicable on object detection models that can provide instance
        segmentation results. It is ignored on on all model types. Possible values are "true" to include the compressed
        RLE string, or "false" to exclude it.>br> The default value is "false" if the parameter is not provided.

        containPolygon: (optional) Flag parameter to request inclusion of the polygon boundary information in object
        detection segmentaion results. This parameter is only applicable on object detection models that can provide
        instance segmentation results. It is ignored on on all model types. Possible values are "true" to include the
        polygon information, or "false" to exclude it. The default value is "true" if the parameter is not provided.

        confthre: (optional) Parameter to specify the confidence threshold to use when providing results. This parameter
        applies to both classification and object detection models. It is a floating point value that specifies the
        threshold at which possible matches are to be excluded from the result set. A value of 0.5 will exclude possible
        matches with a confidence score below 50%. Possible values range from 0.0 to 0.9. The default value is 0.0 if
        this parameter is not specified.

        clsnum: (optional) This parameter is used to identify how many different possible matches are included in the
        results. For classification, this means that if there are multiple possible matches with a confidence score
        above the confthre value, up to the indicated value matches are included in the result. Values are integer
        values where 0 is the default (which means to include all possible matches in the results).

        waitForResults: (optional) This parameter is used for video inferencing. By default, video inference results are
        reported asynchronously -- meaning that the call to do the inference will return while processing continues on
        the video. Inference results are available via the /inferences endpoint. If this parameter is passed with a
        value of "true" (case is ignored), the endpoint will not return until the video has completed processing. The
        JSON results will be returned at that time. Note that the JSON results will also be available via the
        VideoInferences class.

        genCaption: (optional) This parameter is used for video inferencing. It controls whether or not a "captioned"
        video should be generated and stored with the inferencing results. The default varies by the detection being
        done. For Action Detection, the default is to generate a captioned video. For Object Detection, the default
        is to NOT generate a captioned video. The captioned video is accessible via the VideoInferences class.

        :return: Dictionary of model results
        """

        message = self.path + f"dlapis/{model_id}"
        data = {key: value for key, value in kwargs.items()}

        return json.loads(res.post(message, files={'files': open(image_path, 'rb')}, data=data).text)


class VideoInferences(Inferences):

    def __init__(self, username: str, password: str):
        super().__init__()
        self.token = tokens.Token(path=self.path, username=username, password=password)

    def retrieve_all(self, **kwargs) -> dict:
        """
        Retrieves all active and completed video inference results. Video inferences are Action Detection inferences
        and Video Object Detection inferences. Results are ordered by creation date, oldest to newest.

        :return: Dictionary of all inference results
        """

        message = self.path + f"inferences"

        for index, value in enumerate(kwargs):
            if index == 0:
                message += f'?{value}={kwargs[value]}'
            else:
                message += f'&{value}={kwargs[value]}'

        return json.loads(res.get(message, headers={'X-Auth-Token': self.token.get_token()}).text)
