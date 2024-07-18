import warnings
# Suppress all warnings
warnings.filterwarnings("ignore")
import yfinance as yf
import numpy as np
from playwright.sync_api import sync_playwright

# List of Nifty 500 stocks (this is a subset, replace with the complete list)
nifty_500_tickers = ["360ONE.NS", "3MINDIA.NS", "ABB.NS", "ACC.NS", "AIAENG.NS", "APLAPOLLO.NS", "AUBANK.NS", "AARTIIND.NS", "AAVAS.NS", "ABBOTINDIA.NS", "ACE.NS", "ADANIENSOL.NS", "ADANIENT.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "ADANIPOWER.NS", "ATGL.NS", "AWL.NS", "ABCAPITAL.NS", "ABFRL.NS", "AEGISLOG.NS", "AETHER.NS", "AFFLE.NS", "AJANTPHARM.NS", "APLLTD.NS", "ALKEM.NS", "ALKYLAMINE.NS", "ALLCARGO.NS", "ALOKINDS.NS", "ARE&M.NS", "AMBER.NS", "AMBUJACEM.NS", "ANANDRATHI.NS", "ANGELONE.NS", "ANURAS.NS", "APARINDS.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS", "APTUS.NS", "ACI.NS", "ASAHIINDIA.NS", "ASHOKLEY.NS", "ASIANPAINT.NS", "ASTERDM.NS", "ASTRAZEN.NS", "ASTRAL.NS", "ATUL.NS", "AUROPHARMA.NS", "AVANTIFEED.NS", "DMART.NS", "AXISBANK.NS", "BEML.NS", "BLS.NS", "BSE.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BAJAJHLDNG.NS", "BALAMINES.NS", "BALKRISIND.NS", "BALRAMCHIN.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", "MAHABANK.NS", "BATAINDIA.NS", "BAYERCROP.NS", "BERGEPAINT.NS", "BDL.NS", "BEL.NS", "BHARATFORG.NS", "BHEL.NS", "BPCL.NS", "BHARTIARTL.NS", "BIKAJI.NS", "BIOCON.NS", "BIRLACORPN.NS", "BSOFT.NS", "BLUEDART.NS", "BLUESTARCO.NS", "BBTC.NS", "BORORENEW.NS", "BOSCHLTD.NS", "BRIGADE.NS", "BRITANNIA.NS", "MAPMYINDIA.NS", "CCL.NS", "CESC.NS", "CGPOWER.NS", "CIEINDIA.NS", "CRISIL.NS", "CSBBANK.NS", "CAMPUS.NS", "CANFINHOME.NS", "CANBK.NS", "CAPLIPOINT.NS", "CGCL.NS", "CARBORUNIV.NS", "CASTROLIND.NS", "CEATLTD.NS", "CELLO.NS", "CENTRALBK.NS", "CDSL.NS", "CENTURYPLY.NS", "CENTURYTEX.NS", "CERA.NS", "CHALET.NS", "CHAMBLFERT.NS", "CHEMPLASTS.NS", "CHENNPETRO.NS", "CHOLAHLDNG.NS", "CHOLAFIN.NS", "CIPLA.NS", "CUB.NS", "CLEAN.NS", "COALINDIA.NS", "COCHINSHIP.NS", "COFORGE.NS", "COLPAL.NS", "CAMS.NS", "CONCORDBIO.NS", "CONCOR.NS", "COROMANDEL.NS", "CRAFTSMAN.NS", "CREDITACC.NS", "CROMPTON.NS", "CUMMINSIND.NS", "CYIENT.NS", "DCMSHRIRAM.NS", "DLF.NS", "DOMS.NS", "DABUR.NS", "DALBHARAT.NS", "DATAPATTNS.NS", "DEEPAKFERT.NS", "DEEPAKNTR.NS", "DELHIVERY.NS", "DEVYANI.NS", "DIVISLAB.NS", "DIXON.NS", "LALPATHLAB.NS", "DRREDDY.NS", "EIDPARRY.NS", "EIHOTEL.NS", "EPL.NS", "EASEMYTRIP.NS", "EICHERMOT.NS", "ELECON.NS", "ELGIEQUIP.NS", "EMAMILTD.NS", "ENDURANCE.NS", "ENGINERSIN.NS", "EQUITASBNK.NS", "ERIS.NS", "ESCORTS.NS", "EXIDEIND.NS", "FDC.NS", "NYKAA.NS", "FEDERALBNK.NS", "FACT.NS", "FINEORG.NS", "FINCABLES.NS", "FINPIPE.NS", "FSL.NS", "FIVESTAR.NS", "FORTIS.NS", "GAIL.NS", "GMMPFAUDLR.NS", "GMRINFRA.NS", "GRSE.NS", "GICRE.NS", "GILLETTE.NS", "GLAND.NS", "GLAXO.NS", "GLS.NS", "GLENMARK.NS", "MEDANTA.NS", "GPIL.NS", "GODFRYPHLP.NS", "GODREJCP.NS", "GODREJIND.NS", "GODREJPROP.NS", "GRANULES.NS", "GRAPHITE.NS", "GRASIM.NS", "GESHIP.NS", "GRINDWELL.NS", "GAEL.NS", "FLUOROCHEM.NS", "GUJGASLTD.NS", "GMDCLTD.NS", "GNFC.NS", "GPPL.NS", "GSFC.NS", "GSPL.NS", "HEG.NS", "HBLPOWER.NS", "HCLTECH.NS", "HDFCAMC.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HFCL.NS", "HAPPSTMNDS.NS", "HAPPYFORGE.NS", "HAVELLS.NS", "HEROMOTOCO.NS", "HSCL.NS", "HINDALCO.NS", "HAL.NS", "HINDCOPPER.NS", "HINDPETRO.NS", "HINDUNILVR.NS", "HINDZINC.NS", "POWERINDIA.NS", "HOMEFIRST.NS", "HONASA.NS", "HONAUT.NS", "HUDCO.NS", "ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS", "ISEC.NS", "IDBI.NS", "IDFCFIRSTB.NS", "IDFC.NS", "IIFL.NS", "IRB.NS", "IRCON.NS", "ITC.NS", "ITI.NS", "INDIACEM.NS", "IBULHSGFIN.NS", "INDIAMART.NS", "INDIANB.NS", "IEX.NS", "INDHOTEL.NS", "IOC.NS", "IOB.NS", "IRCTC.NS", "IRFC.NS", "INDIGOPNTS.NS", "IGL.NS", "INDUSTOWER.NS", "INDUSINDBK.NS", "NAUKRI.NS", "INFY.NS", "INOXWIND.NS", "INTELLECT.NS", "INDIGO.NS", "IPCALAB.NS", "JBCHEPHARM.NS", "JKCEMENT.NS", "JBMA.NS", "JKLAKSHMI.NS", "JKPAPER.NS", "JMFINANCIL.NS", "JSWENERGY.NS", "JSWINFRA.NS", "JSWSTEEL.NS", "JAIBALAJI.NS", "J&KBANK.NS", "JINDALSAW.NS", "JSL.NS", "JINDALSTEL.NS", "JIOFIN.NS", "JUBLFOOD.NS", "JUBLINGREA.NS", "JUBLPHARMA.NS", "JWL.NS", "JUSTDIAL.NS", "JYOTHYLAB.NS", "KPRMILL.NS", "KEI.NS", "KNRCON.NS", "KPITTECH.NS", "KRBL.NS", "KSB.NS", "KAJARIACER.NS", "KPIL.NS", "KALYANKJIL.NS", "KANSAINER.NS", "KARURVYSYA.NS", "KAYNES.NS", "KEC.NS", "KFINTECH.NS", "KOTAKBANK.NS", "KIMS.NS", "LTF.NS", "LTTS.NS", "LICHSGFIN.NS", "LTIM.NS", "LT.NS", "LATENTVIEW.NS", "LAURUSLABS.NS", "LXCHEM.NS", "LEMONTREE.NS", "LICI.NS", "LINDEINDIA.NS", "LLOYDSME.NS", "LUPIN.NS", "MMTC.NS", "MRF.NS", "MTARTECH.NS", "LODHA.NS", "MGL.NS", "MAHSEAMLES.NS", "M&MFIN.NS", "M&M.NS", "MHRIL.NS", "MAHLIFE.NS", "MANAPPURAM.NS", "MRPL.NS", "MANKIND.NS", "MARICO.NS", "MARUTI.NS", "MASTEK.NS", "MFSL.NS", "MAXHEALTH.NS", "MAZDOCK.NS", "MEDPLUS.NS", "METROBRAND.NS", "METROPOLIS.NS", "MINDACORP.NS", "MSUMI.NS", "MOTILALOFS.NS", "MPHASIS.NS", "MCX.NS", "MUTHOOTFIN.NS", "NATCOPHARM.NS", "NBCC.NS", "NCC.NS", "NHPC.NS", "NLCINDIA.NS", "NMDC.NS", "NSLNISP.NS", "NTPC.NS", "NH.NS", "NATIONALUM.NS", "NAVINFLUOR.NS", "NESTLEIND.NS", "NETWORK18.NS", "NAM-INDIA.NS", "NUVAMA.NS", "NUVOCO.NS", "OBEROIRLTY.NS", "ONGC.NS", "OIL.NS", "OLECTRA.NS", "PAYTM.NS", "OFSS.NS", "POLICYBZR.NS", "PCBL.NS", "PIIND.NS", "PNBHOUSING.NS", "PNCINFRA.NS", "PVRINOX.NS", "PAGEIND.NS", "PATANJALI.NS", "PERSISTENT.NS", "PETRONET.NS", "PHOENIXLTD.NS", "PIDILITIND.NS", "PEL.NS", "PPLPHARMA.NS", "POLYMED.NS", "POLYCAB.NS", "POONAWALLA.NS", "PFC.NS", "POWERGRID.NS", "PRAJIND.NS", "PRESTIGE.NS", "PRINCEPIPE.NS", "PRSMJOHNSN.NS", "PGHH.NS", "PNB.NS", "QUESS.NS", "RRKABEL.NS", "RBLBANK.NS", "RECLTD.NS", "RHIM.NS", "RITES.NS", "RADICO.NS", "RVNL.NS", "RAILTEL.NS", "RAINBOW.NS", "RAJESHEXPO.NS", "RKFORGE.NS", "RCF.NS", "RATNAMANI.NS", "RTNINDIA.NS", "RAYMOND.NS", "REDINGTON.NS", "RELIANCE.NS", "RBA.NS", "ROUTE.NS", "SBFC.NS", "SBICARD.NS", "SBILIFE.NS", "SJVN.NS", "SKFINDIA.NS", "SRF.NS", "SAFARI.NS", "MOTHERSON.NS", "SANOFI.NS", "SAPPHIRE.NS", "SAREGAMA.NS", "SCHAEFFLER.NS", "SCHNEIDER.NS", "SHREECEM.NS", "RENUKA.NS", "SHRIRAMFIN.NS", "SHYAMMETL.NS", "SIEMENS.NS", "SIGNATURE.NS", "SOBHA.NS", "SOLARINDS.NS", "SONACOMS.NS", "SONATSOFTW.NS", "STARHEALTH.NS", "SBIN.NS", "SAIL.NS", "SWSOLAR.NS", "STLTECH.NS", "SUMICHEM.NS", "SPARC.NS", "SUNPHARMA.NS", "SUNTV.NS", "SUNDARMFIN.NS", "SUNDRMFAST.NS", "SUNTECK.NS", "SUPREMEIND.NS", "SUVENPHAR.NS", "SUZLON.NS", "SWANENERGY.NS", "SYNGENE.NS", "SYRMA.NS", "TV18BRDCST.NS", "TVSMOTOR.NS", "TVSSCS.NS", "TMB.NS", "TANLA.NS", "TATACHEM.NS", "TATACOMM.NS", "TCS.NS", "TATACONSUM.NS", "TATAELXSI.NS", "TATAINVEST.NS", "TATAMTRDVR.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS", "TATATECH.NS", "TTML.NS", "TECHM.NS", "TEJASNET.NS", "NIACL.NS", "RAMCOCEM.NS", "THERMAX.NS", "TIMKEN.NS", "TITAGARH.NS", "TITAN.NS", "TORNTPHARM.NS", "TORNTPOWER.NS", "TRENT.NS", "TRIDENT.NS", "TRIVENI.NS", "TRITURBINE.NS", "TIINDIA.NS", "UCOBANK.NS", "UNOMINDA.NS", "UPL.NS", "UTIAMC.NS", "UJJIVANSFB.NS", "ULTRACEMCO.NS", "UNIONBANK.NS", "UBL.NS", "UNITDSPR.NS", "USHAMART.NS", "VGUARD.NS", "VIPIND.NS", "VAIBHAVGBL.NS", "VTL.NS", "VARROC.NS", "VBL.NS", "MANYAVAR.NS", "VEDL.NS", "VIJAYA.NS", "IDEA.NS", "VOLTAS.NS", "WELCORP.NS", "WELSPUNLIV.NS", "WESTLIFE.NS", "WHIRLPOOL.NS", "WIPRO.NS", "YESBANK.NS", "ZFCVINDIA.NS", "ZEEL.NS", "ZENSARTECH.NS", "ZOMATO.NS", "ZYDUSLIFE.NS", "ECLERX.NS"]  # Add all Nifty 500 tickers here

# McGinley Dynamic calculation function using numpy
def calculate_mcginley_dynamic(prices, period):
    md = np.empty(len(prices))
    md[0] = prices[0]  # Initialize with the first value
    for i in range(1, len(prices)):
        md[i] = md[i - 1] + (prices[i] - md[i - 1]) / min(2 * period, (prices[i] / md[i - 1]) ** 4)
    return md

# Fetch daily data for a given ticker
def fetch_daily_data(ticker):
    data = yf.download(ticker, period="1y", interval='1d')  # Fetch last 1 year of daily data
    data = data[['Close']]
    return data

# Check for crossover with McGinley Dynamic
def check_mcginley_crossover(ticker):
    data = fetch_daily_data(ticker)
    close_prices = data['Close'].values
    mcginley = calculate_mcginley_dynamic(close_prices, 21)
    
    # Check if the last close price crosses above the McGinley Dynamic
    if close_prices[0] > mcginley[0] and close_prices[-1] <= mcginley[-1]:
        return True
    return False

# List stocks that cross the McGinley Dynamic
crossing_stocks = []

for ticker in nifty_500_tickers:
    if check_mcginley_crossover(ticker):
        crossing_stocks.append(ticker)

# Print the list of stocks
print("Stocks crossing McGinley Dynamic 21 on one-day chart:", crossing_stocks)

# Example of using Playwright for an additional web scraping task (if needed)
def scrape_example():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://example.com')
        # Perform any scraping tasks here
        browser.close()

# Call scrape_example() if you need to perform additional web scraping
# scrape_example()
