import streamlit as st
import pandas as pd
import random

MENU_PATH = './menu.csv'

menu = pd.read_csv(MENU_PATH, index_col=0)


def gacha(max_price, max_calorie):
    lottery_ids = list(menu.index)
    result_ids = []
    total = {'price':0, 'calorie':0, 'salt':0}

    while(total['price'] < max_price and total['calorie'] < max_calorie \
          and len(lottery_ids) != 0):
        selected_id = random.choice(lottery_ids)
        selected_food = menu.loc[selected_id]
        if total['price'] + selected_food.price <= max_price \
           and total['calorie'] + selected_food.calorie <= max_calorie:
            result_ids.append(selected_id)
            total['price'] += selected_food.price
            total['calorie'] += selected_food.calorie
            total['salt'] += selected_food.salt

        lottery_ids.remove(selected_id)

    return result_ids, total


def view():
    st.title('学食メニュー組合せ機🍚')

    c_top = st.container()

    c_button = st.empty()

    st.subheader('設定')
    price_input = st.number_input(
        '予算上限を決めてください（円）',
        300, 3000, 1000, 100,
    )

    calorie_input = float('inf')
    if st.checkbox('カロリーを気にする方へ'):
        calorie_input = st.number_input(
            'カロリー上限を決めてください（kcal）',
            400, 3000, 700, 100,
        )

    if c_button.button('メニューを決める'):
        result_ids, total = gacha(price_input, calorie_input)
        c_top.write(menu.loc[result_ids].style.format({'salt':'{:.1f}'}))
        c_top.info("合計 {}円 {}kcal 塩分 {}g".format(int(total['price']), int(total['calorie']), round(total['salt'],1)))

    with st.expander('メニューを表示'):
        st.subheader('メニュー表')
        st.write(menu.style.format({'salt':'{:.1f}'}))


view()