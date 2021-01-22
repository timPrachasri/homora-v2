from brownie import accounts, Contract, chain
try:
    from brownie import interface
except:
    pass

USDT = '0xdac17f958d2ee523a2206206994597c13d831ec7'
USDC = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
DAI = '0x6b175474e89094c44da98b954eedeac495271d0f'
ADAI = '0x028171bCA77440897B824Ca71D1c56caC55b68A3'
AUSDC = '0xBcca60bB61934080951369a648Fb03DF4F96263C'
AUSDT = '0x3Ed3B47Dd13EC9a98b44e6204A523E766B225811'
WETH = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
SUSD = '0x57ab1ec28d129707052df4df418d58a2d46d5f51'
HUSD = '0xdf574c24545e5ffecb9a659c229253d4111d87e1'
BUSD = '0x4fabb145d64652a948d72533023f6e7a623c7c53'
DPI = '0x1494ca1f11d487c2bbe4543e90080aeba4ba3c2b'
YDAI = '0xC2cB1040220768554cf699b0d863A3cd4324ce32'
YUSDT = '0xE6354ed5bC4b393a5Aad09f21c46E101e692d447'
YUSDC = '0x26EA744E5B887E5205727f55dFBE8685e3b21951'
YBUSD = '0x04bC0Ab673d88aE9dbC9DA2380cB6B79C4BCa9aE'
WBTC = '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599'
RENBTC = '0xeb4c2781e4eba804ce9a9803c67d0893436bb27d'
PERP = '0xbC396689893D065F41bc2C6EcbeE5e0085233447'
DFD = '0x20c36f062a31865bED8a5B1e512D9a1A20AA333A'
DUSD = '0x5bc25f649fc4e26069ddf4cf4010f9f706c23831'
EURS = '0xdb25f211ab05b1c97d595516f45794528a807ad8'
SEUR = '0xd71ecff9342a5ced620049e616c5035f1db98620'

UNI_WETH_DAI = '0xa478c2975ab1ea89e8196811f51a7b7ade33eb11'
UNI_WETH_WBTC = '0xbb2b8038a1640196fbe3e38816f3e67cba72d940'
UNI_WETH_USDT = '0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852'
UNI_WETH_USDC = '0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc'
UNI_WETH_DPI = '0x4d5ef58aac27d99935e5b6b4a6778ff292059991'
UNI_WETH_PERP = '0xf66369997ae562bc9eec2ab9541581252f9ca383'


def is_uni_lp(token):
    return token.symbol() == 'UNI-V2'


def is_sushi_lp(token):
    return token.symbol() == 'SLP'


def is_bal_lp(token):
    return token.symbol() == 'BPT'


def is_crv_lp(token):
    return token.name()[:8] == 'Curve.fi'


def mint_tokens(token, to, interface=None, amount=None):
    if interface is None:
        interface = globals()['interface']

    if amount is None:
        # default is 1M tokens
        amount = 10**12 * 10**token.decimals()

    if token == USDT:
        owner = token.owner()
        token.issue(amount, {'from': owner})
        token.transfer(to, amount, {'from': owner})
    elif token == USDC:
        master_minter = token.masterMinter()
        token.configureMinter(master_minter, 2**256-1, {'from': master_minter})
        token.mint(to, amount, {'from': master_minter})
    elif token == DAI:
        auth = '0x9759a6ac90977b93b58547b4a71c78317f391a28'
        token.mint(to, amount, {'from': auth})
    elif token == AUSDT:
        pool = '0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9'
        token.mint(to, amount, 10**18, {'from': pool})
    elif token == AUSDC:
        pool = '0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9'
        token.mint(to, amount, 10**18, {'from': pool})
    elif token == ADAI:
        pool = '0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9'
        token.mint(to, amount, 10**18, {'from': pool})
    elif token == WETH:
        token.deposit({'from': to, 'value': amount})
    elif token == SUSD:
        target = interface.IERC20Ex(token.target())
        issuer = '0x611Abc0e066A01AFf63910fC8935D164267eC6CF'
        target.issue(to, amount, {'from': issuer})
    elif token == HUSD:
        issuer = '0xc2fbf9b9084e92f9649ca4cec9043daac9092539'
        token.issue(to, amount, {'from': issuer})
    elif token == BUSD:
        supply_controller = token.supplyController()
        token.increaseSupply(amount, {'from': supply_controller})
        token.transfer(to, amount, {'from': supply_controller})
    elif token == YDAI:
        mint_tokens(interface.IERC20Ex(DAI), to, amount)
        interface.IERC20Ex(DAI).approve(token, 0, {'from': to})
        interface.IERC20Ex(DAI).approve(token, 2**256-1, {'from': to})
        token.deposit(amount, {'from': to})
    elif token == YUSDT:
        mint_tokens(interface.IERC20Ex(USDT), to, amount)
        interface.IERC20Ex(USDT).approve(token, 0, {'from': to})
        interface.IERC20Ex(USDT).approve(token, 2**256-1, {'from': to})
        token.deposit(amount, {'from': to})
    elif token == YBUSD:
        mint_tokens(interface.IERC20Ex(BUSD), to, amount)
        interface.IERC20Ex(BUSD).approve(token, 0, {'from': to})
        interface.IERC20Ex(BUSD).approve(token, 2**256-1, {'from': to})
        token.deposit(amount, {'from': to})
    elif token == YUSDC:
        mint_tokens(interface.IERC20Ex(USDC), to, amount)
        interface.IERC20Ex(USDC).approve(token, 0, {'from': to})
        interface.IERC20Ex(USDC).approve(token, 2**256-1, {'from': to})
        token.deposit(amount, {'from': to})
    elif token == DPI:
        module = token.getModules()[0]
        token.mint(to, amount, {'from': module})
    elif token == WBTC:
        owner = token.owner()
        token.mint(to, amount, {'from': owner})
    elif token == RENBTC:
        owner = token.owner()
        token.mint(to, amount, {'from': owner})
    elif token == PERP:
        owner = token.owner()
        token.addMinter(owner, {'from': owner})
        token.mint(to, amount, {'from': owner})
    elif token == DFD:
        gov = token.governance()
        token.mint(to, amount, {'from': gov})
    elif token == DUSD:
        core = token.core()
        token.mint(to, amount, {'from': core})
    elif token == EURS:
        owner = '0x2EbBbc541E8f8F24386FA319c79CedA0579f1Efb'
        token.createTokens(amount, {'from': owner})
        token.transfer(to, amount, {'from': owner})
    elif token == SEUR:
        target = interface.IERC20Ex('0xc61b352fcc311ae6b0301459a970150005e74b3e')
        issuer = '0x611Abc0e066A01AFf63910fC8935D164267eC6CF'
        target.issue(to, amount, {'from': issuer})
    elif is_uni_lp(token):
        router = interface.IUniswapV2Router02('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')
        # Uniswap LP token
        token0 = interface.IERC20Ex(token.token0())
        token1 = interface.IERC20Ex(token.token1())
        # mint underlying
        amount0 = 10**12 * 10**token0.decimals()
        amount1 = 10**12 * 10**token1.decimals()
        mint_tokens(token0, to, amount0)
        mint_tokens(token1, to, amount1)
        # approve router
        token0.approve(router, 0, {'from': to})
        token0.approve(router, 2**256-1, {'from': to})
        token1.approve(router, 0, {'from': to})
        token1.approve(router, 2**256-1, {'from': to})
        # add liquidity
        interface.IUniswapV2Router02(router).addLiquidity(
            token0, token1, amount0, amount1, 0, 0, to, chain.time() + 1200, {'from': to})
    elif is_sushi_lp(token):
        router = interface.IUniswapV2Router02('0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f')
        # Sushiswap LP token
        token0 = interface.IERC20Ex(token.token0())
        token1 = interface.IERC20Ex(token.token1())
        # mint underlying
        amount0 = 10**12 * 10**token0.decimals()
        amount1 = 10**12 * 10**token1.decimals()
        mint_tokens(token0, to, amount0)
        mint_tokens(token1, to, amount1)
        # approve router
        token0.approve(router, 0, {'from': to})
        token0.approve(router, 2**256-1, {'from': to})
        token1.approve(router, 0, {'from': to})
        token1.approve(router, 2**256-1, {'from': to})
        # add liquidity
        interface.IUniswapV2Router02(router).addLiquidity(
            token0, token1, amount0, amount1, 0, 0, to, chain.time() + 1200, {'from': to})
    elif is_bal_lp(token):
        # Balancer LP token
        tokens = token.getFinalTokens()
        max_amts = []
        amt_desired = 10**100
        for _token in tokens:
            _token = interface.IERC20Ex(_token)
            amt = 10**12 * 10**_token.decimals()
            mint_tokens(_token, to, amt)
            _token.approve(token, 0, {'from': to})
            _token.approve(token, 2**256-1, {'from': to})
            max_amts.append(amt)
            amt_desired = min(amt_desired, amt * token.totalSupply() // token.getBalance(_token))
        token.joinPool(amt_desired * 9 // 10, max_amts, {'from': to})
    elif is_crv_lp(token):
        # Curve LP token
        registry = interface.ICurveRegistry('0x7d86446ddb609ed0f5f8684acf30380a356b2b4c')
        pool = registry.get_pool_from_lp_token(token)
        tokens = registry.get_coins(pool)
        amts = []
        for _token in tokens:
            if _token == '0x0000000000000000000000000000000000000000':
                continue
            _token = interface.IERC20Ex(_token)
            amt = 10**6 * 10**_token.decimals()
            prevBal = _token.balanceOf(to)
            mint_tokens(_token, to, amt)
            curBal = _token.balanceOf(to)
            amts.append(curBal - prevBal)
            interface.IERC20Ex(_token).approve(pool, 0, {'from': to})
            interface.IERC20Ex(_token).approve(pool, 2**256-1, {'from': to})
        desc = f'uint[{len(amts)}],uint'
        print('adding liquidity to curve')
        print(amts)
        interface.ICurvePool(pool).add_liquidity[desc](amts, 0, {'from': to})
    else:
        raise Exception('unsupported token')


def update_kp3r_all(interface):
    if interface is None:
        print('===')
        interface = globals()['interface']

    keeper_oracle = interface.IKeep3rV1Oracle('0x73353801921417F465377c8d898c6f4C0270282C')
    keeper_oracle.workForFree({'from': '0xfe56a0dbdad44dd14e4d560632cc842c8a13642b'})
    print('work done 1')
    chain.sleep(1810)
    keeper_oracle.workForFree({'from': '0xfe56a0dbdad44dd14e4d560632cc842c8a13642b'})
    print('work done 2')


def update_kp3r_pairs(interface, pairs):
    if interface is None:
        print('===')
        interface = globals()['interface']

    keeper_oracle = interface.IKeep3rV1Oracle('0x73353801921417F465377c8d898c6f4C0270282C')
    print('doing 1st tx')
    for pair in pairs:
        keeper_oracle.updatePair(pair, {'from': '0xfe56a0dbdad44dd14e4d560632cc842c8a13642b'})
    chain.sleep(1810)
    print('doing 2nd tx')
    for pair in pairs:
        keeper_oracle.updatePair(pair, {'from': '0xfe56a0dbdad44dd14e4d560632cc842c8a13642b'})