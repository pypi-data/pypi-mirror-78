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

    logging.debug(
        "Property ${property_id} requested in {current_mode} mode".format(
            current_mode=('simulation' if self.simulation_mode else 'real')
        )
    )
    try:
        return self.implementation.Get_${property_id}(request, context)
    except SiLAError as err:
        err.raise_rpc_error(context=context)
