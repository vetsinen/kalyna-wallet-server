from kalyna_wallet_lib import generate_cusom_mnemo, get_solana_derived_wallet, get_sol_balance

if __name__ == "__main__":
    text = """
    А ми нашу славну Україну
    Ой у лузі червона калина похилилася
    А ми нашу славну Україну
    Гей, гей, розвеселимо!
    А ми тую червону калину підіймемо
    Чогось наша славна Україна зажурилася
    А ми тую червону калину підіймемо
    """
    custom_mnemonic = generate_cusom_mnemo(text) #червона калина похилилася чогось славна україна зажурилася червону калину підіймемо славну україну
    print(custom_mnemonic)
    wallet_address = (get_solana_derived_wallet(custom_mnemonic)[0])
    print(wallet_address)
    print(get_sol_balance(wallet_address))