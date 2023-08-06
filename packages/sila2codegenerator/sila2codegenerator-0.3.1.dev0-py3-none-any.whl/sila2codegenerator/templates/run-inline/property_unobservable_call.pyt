logging.info(" " * 4 + "Reading unobservable property ${property_id}:")
try:
    response = self.${feature_identifier}_stub.Get_${property_id}(
        ${feature_identifier}_pb2.Get_${property_id}_Parameters()
    )
    logging.debug(
        " " * 8 + 'Get_${property_id} response: {response}'.format(
            response=response
        )
    )
except grpc.RpcError as grpc_err:
    logging.error(" " * 8 + "gRPC/SiLA error: {error}".format(error=grpc_err))
