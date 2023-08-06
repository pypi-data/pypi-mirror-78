logging.info(" " * 4 + "Reading observable property ${property_id}:")
try:
    # define a timeout of 10 seconds in which we read the parameter
    timeout = time.time() + 10.0
    # loop over responses
    for response in self.${feature_identifier}_stub.Subscribe_${property_id}(
            ${feature_identifier}_pb2.Subscribe_${property_id}_Parameters()
    ):
        logging.debug(
            " " * 8 + 'Current response of ${property_id}: {response}'.format(
                response=response
            )
        )

        if time.time() > timeout:
            print('Timeout')
            break

except grpc.RpcError as grpc_err:
    logging.error(" " * 8 + "gRPC/SiLA error: {error}".format(error=grpc_err))
