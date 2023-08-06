def Subscribe_${property_id}(self) \
        -> ${feature_identifier}_pb2.Subscribe_${property_id}_Responses:
    """Wrapper to get property ${property_id} from the server."""
    # noinspection PyUnusedLocal - type definition, just for convenience
    grpc_err: grpc.Call

    logging.debug("Reading observable property ${property_id}:")
    try:
        response = self.${feature_identifier}_stub.Subscribe_${property_id}(
            ${feature_identifier}_pb2.Subscribe_${property_id}_Parameters()
        )
        logging.debug(
            'Subscribe_${property_id} response: {response}'.format(
                response=response
            )
        )
    except grpc.RpcError as grpc_err:
        self.grpc_error_handling(grpc_err)
        return None

    return response
