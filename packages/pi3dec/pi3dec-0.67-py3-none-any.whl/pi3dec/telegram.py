from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot

import pi3dec
import pandas as pd, numpy as np
import time, os
import matplotlib.pyplot as plt

pe = pi3dec.Experiment("Apr26/", connect=False)

TOKEN = "975339008:AAEL0t2zptXl-Ghb5TZwgWekACo627RVuf4" # pm12
# TOKEN = "948747373:AAGh6dPtT1_vGgze5AhapaNjCFAujfztolI"  # pm13

IDs = {519022449, 623255444, 946308959, 190185464}
EXP_DIR = "Apr26"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize the experiment and the bot
bot = Bot(TOKEN)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hola! This is Incubot for the CLAN lab.')
    update.message.reply_text('Before changing volumes make sure your ID is registered.')
    update.message.reply_text('Send /help for help. Enjoy!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        'Send:\n/plot start end i,j,k... \nto get a plot of cultures No. i, j, k...\n' +
        "from the time moment start  till the end. \nExample:\n/plot 5h 1w 0,1,2,3,4,5,6\n" +
        "plots the OD in 0th, 1st, ..., 6th tubes from t=5h to t = 1week \n\n" +
        "/pumpdata for pump_data.csv\n/rawsignal for raw_signal.csv\n\n" +
        "/getvolumes to get death volumes\n" +
        "/getthresholds to get thresholds\n" +
        "/lastdata\n" +
        "/setvolumes 0,1,2,3,4,5,6 to change volumes. Only for the registered IDs!\n" +
        "/setthresholds 0,1,2,3,4,5,6 to change thresholds. Only for the registered IDs!\n" +
        "/plotOD\n /convertODs \n/setconditions tube,vol,ODraw"
    )


def sorry(update, context):
    """Apologize"""
    update.message.reply_text('Unknown command.')
    print(context)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def plot(update, context):
    """Send plot"""
    bot = Bot(TOKEN)
    update.message.reply_text('Please wait')
    chat_id = update.message.chat_id
    os.system("raspistill -o botpic.png")
    bot.send_photo(chat_id=chat_id, photo=open("botpic.png", 'rb'))


def plotOD(update, context):
    t = context.args[0].replace(" ", "")
    t = int(t)
    """Send plot"""
    bot = Bot(TOKEN)
    update.message.reply_text('Please wait')
    chat_id = update.message.chat_id
    plot_OD(t)

    photopath = EXP_DIR + '/botplot.png'
    bot.send_photo(chat_id=chat_id, photo=open(photopath, 'rb'))


def pumpdata(update, context):
    """Get pump data"""
    chat_id = update.message.chat_id
    bot.send_document(chat_id=chat_id, document=open(EXP_DIR + '/pump_data.csv', 'rb'))


def rawsignal(update, context):
    """Get raw signal"""
    chat_id = update.message.chat_id
    bot.send_document(chat_id=chat_id, document=open(EXP_DIR + '/raw_signal.csv', 'rb'))


def setvolumes(update, context):
    """Define death volumes"""
    try:
        death_volumes = context.args[0].replace(' ', '').split(',')
        death_volumes = [float(i) for i in death_volumes]
        #         for i in range(7):
        #             _ = death_volumes[i] + 1
        with open(EXP_DIR + '/death_volumes.csv', 'w') as death_csv:
            death_csv.write(','.join(str(i) for i in death_volumes))
        update.message.reply_text('Successfully changed death volumes to '
                                  + ','.join(str(i) for i in death_volumes))
    except:
        update.message.reply_text('Invalid data.')


def getvolumes(update, context):
    """Get death volumes"""
    chat_id = update.message.chat_id
    try:
        text = open(EXP_DIR + '/death_volumes.csv', 'r').read()
        update.message.reply_text(text)

        bot.send_document(chat_id=chat_id, document=open(EXP_DIR + '/death_volumes.csv', 'rb'))
    except:
        update.message.reply_text('No such file!')


def getthresholds(update, context):
    """Get thresholds"""
    chat_id = update.message.chat_id
    try:
        text = open(EXP_DIR + '/thresholds.csv', 'r').read()
        update.message.reply_text(text)

        bot.send_document(chat_id=chat_id, document=open(EXP_DIR + '/thresholds.csv', 'rb'))
    except:
        update.message.reply_text('No such file!')


def set_one_volume(tube, value):
    assert tube in [0, 1, 2, 3, 4, 5, 6]
    assert value <= 10
    value = float(value)
    volumes = pd.read_csv(EXP_DIR + '/death_volumes.csv', header=None).values[0]
    volumes[tube] = value
    volumes_df = pd.DataFrame(volumes).T
    volumes_df.to_csv(EXP_DIR + '/death_volumes.csv', header=None, index=None)


def raw_to_OD(meas, maximum):
    meas = np.array(meas)
    maximum = np.array(maximum)
    return 0.4 * (meas - maximum) / (11500 - maximum)


def OD_to_raw(OD, maximum):
    OD = np.array(OD)
    maximum = np.array(maximum)
    meas = OD * (11500 - maximum) / 0.4 + maximum
    return meas.astype(int)


def set_one_threshold(tube, value):
    assert tube in [0, 1, 2, 3, 4, 5, 6]
    assert value > 0.15
    try:
        thresholds = pd.read_csv(EXP_DIR + '/thresholds.csv', header=None).values[0]
    except FileNotFoundError:
        thresholds = [1, 1, 1, 1, 1, 1, 1]
        with open(EXP_DIR + '/thresholds.csv', 'w') as thresholds_csv:
            thresholds_csv.write(','.join(str(i) for i in thresholds))

    thresholds[tube] = value
    thresholds_df = pd.DataFrame(thresholds).T
    thresholds_df.to_csv(EXP_DIR + '/thresholds.csv', header=None, index=None)


def setthresholds(update, context):
    """Define death volumes"""

    try:
        thresholds = context.args[0].replace(' ', '').split(',')
        thresholds = np.array([float(i) for i in thresholds])
        assert len(thresholds) == 7
        for t in range(7):
            set_one_threshold(t, thresholds[t])
        update.message.reply_text('Successfully changed thresholds to '
                                  + ','.join(str(i) for i in thresholds))
    except:
        update.message.reply_text('Invalid data.')


def setconditions(update, context):
    """Define one death volume"""

    try:
        conditions = context.args[0].replace(' ', '').split(',')
        conditions = [float(i) for i in conditions]
        assert len(conditions) == 3
        t, volume, threshold = conditions
        t = int(t)
        threshold = int(threshold)
        assert t in [0, 1, 2, 3, 4, 5, 6]
        assert volume < 10
        set_one_threshold(t, threshold)
        set_one_volume(t, volume)
        update.message.reply_text(
            'Tube %d will be diluted with %.1f ml Death and %.1f ml Peace at OD=%d (raw OD measurement)' % (
            t, volume, 10 - volume, threshold))
    except:
        update.message.reply_text('Invalid data.')


def lastdata(update, context):
    pe.df_update()
    time = pe.df.iloc[-1, 0]
    lastvals = np.array(pe.df.iloc[-1, 1::4])
    string = str(time) + "\nrawODs: " + ", ".join(str(i) for i in lastvals)
    update.message.reply_text('Last measurements:\n%s' % string)


def convertODs(update, context):
    ODs = context.args[0].replace(' ', '').split(',')
    ODs = [float(i) for i in ODs]
    raw_values = OD_to_raw(ODs, maximum=nullODs)

    ODs_str = ','.join(str(i) for i in ODs)
    raw_values_str = ','.join(str(i) for i in raw_values)
    update.message.reply_text('OD values of %s\ncorrespond to raw measurements of:\n%s' % (ODs_str, raw_values_str))


# Define Updater
updater = Updater(TOKEN, use_context=True)
# Get the dispatcher to register handlers
dp = updater.dispatcher

# on different commands - answer in Telegram
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("plot", plot))
dp.add_handler(CommandHandler("plotOD", plotOD))
dp.add_handler(CommandHandler("pumpdata", pumpdata))
dp.add_handler(CommandHandler("rawsignal", rawsignal))
dp.add_handler(CommandHandler("getvolumes", getvolumes))
dp.add_handler(CommandHandler("getthresholds", getthresholds))
dp.add_handler(CommandHandler("convertODs", convertODs))
dp.add_handler(CommandHandler("lastdata", lastdata))

# Private
dp.add_handler(CommandHandler("setvolumes", setvolumes, filters=Filters.user(user_id=list(IDs))))
dp.add_handler(CommandHandler("setthresholds", setthresholds, filters=Filters.user(user_id=list(IDs))))
dp.add_handler(CommandHandler("setconditions", setconditions, filters=Filters.user(user_id=list(IDs))))

# Unknown command
dp.add_handler(MessageHandler(Filters.text, sorry))

# log all errors
dp.add_error_handler(error)

# Start the Bot
updater.start_polling()
