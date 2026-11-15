def predict_violation(is_verified_seller: bool, images_qty: int) -> bool:
    return not is_verified_seller and images_qty == 0