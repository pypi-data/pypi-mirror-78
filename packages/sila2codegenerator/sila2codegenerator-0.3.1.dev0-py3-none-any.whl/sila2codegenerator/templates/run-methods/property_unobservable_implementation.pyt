def Get_${property_id}(self, request, context: grpc.ServicerContext) \
        -> ${feature_identifier}_pb2.Get_${property_id}_Responses:
    """
    Requests the unobservable property ${property_name}
${indent(8):trim(True,False):property_description}

    :param request: An empty gRPC request object (properties have no parameters)
    :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

    :returns: A response object with the following fields:
${indent(8):trim(True,False):response_description}
    """

    # initialise the return value
    return_value: ${feature_identifier}_pb2.Get_${property_id}_Responses = None

    # TODO:
    #   Add implementation of ${implementation_mode} for property ${property_id} here and write the resulting response
    #   in return_value

    # fallback to default
    if return_value is None:
        return_value = ${feature_identifier}_pb2.Get_${property_id}_Responses(
            **default_dict['Get_${property_id}_Responses']
        )

    return return_value