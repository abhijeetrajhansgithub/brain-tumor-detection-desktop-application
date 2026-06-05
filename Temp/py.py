def run():
    from Models.load_model import GET_MODEL_PATHS__for_btcm_mdl_v01s, GET_MODEL_PATHS__for_btcm_mdl_21ms

    h5_MODEL_path, keras_MODEL_path = GET_MODEL_PATHS__for_btcm_mdl_v01s()
    print(h5_MODEL_path, keras_MODEL_path)

    h5_MODEL_path, keras_MODEL_path = GET_MODEL_PATHS__for_btcm_mdl_21ms()
    print(h5_MODEL_path, keras_MODEL_path)



    return

if __name__ == "__main__":
    run()