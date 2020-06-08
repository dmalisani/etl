
def data_extractor(batch_data: list) -> list:
    for item in batch_data:
        item.update({"proc": True})
    return batch_data
