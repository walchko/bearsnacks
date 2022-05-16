import torchinfo

def summary(model):
    print(torchinfo.summary(
        model,
        col_names=["kernel_size", "num_params"],
        row_settings=["var_names"]
    ))