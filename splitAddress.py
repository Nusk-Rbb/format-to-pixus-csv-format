import requests
from pprint import pprint
import pandas as pd

def get_street_by_address(prefecture, city, address):
    street = address.split(prefecture)[1].split(city)[1]
    return street

def get_address_by_postal_code(zipcode):
    url = "https://zipcloud.ibsnet.co.jp/api/search"
    query = {
        "zipcode": zipcode
    }
    response = requests.get(url, params=query)
    data = response.json()
    return data

def main():
    # CSVファイルを指定
    input_file = "address2025.csv"
    # input_file = "test_address.csv"
    output_file = "pixus_new_receivers.csv"
    # output_file = "test_output.csv"
    # CSVファイルを読み込む
    # df = pd.read_csv("address2025.csv", encoding="shift-jis")
    input_df = pd.read_csv(input_file, encoding="shift-jis")
    output_df = pd.read_csv(output_file, encoding="shift-jis")


    new_data  = []
    input = {
        "name": input_df["氏名"],
        "honor": input_df["敬称"],
        "hurigana": input_df["フリガナ"],
        "joint_name": input_df["氏名(連名１)"],
        "postal": input_df["郵便番号"],
        "address": input_df["住所1"],
        "building": input_df["住所2"],
    }

    # 1.郵便番号と住所から都道府県、市区町村、それ以外を抽出し、
    # 2.CSVファイルに書き込む
    for postal_code, address, building, name, joint_name, honor, hurigana in zip(
        input["postal"],
        input["address"],
        input["building"],
        input["name"], 
        input["joint_name"], 
        input["honor"], 
        input["hurigana"]):
        # 郵便番号と住所から都道府県、市区町村、それ以外を抽出
        address_from_postal = get_address_by_postal_code(postal_code)
        prefecture = address_from_postal["results"][0]["address1"]
        city = address_from_postal["results"][0]["address2"]
        street_no = get_street_by_address(prefecture, city, address)

        if(pd.isnull(joint_name)):
            joint_name = ""

        if(pd.isnull(building)):
            building = ""

        print(name, hurigana, joint_name, honor, prefecture, city, street_no, building)
        # CSVファイルに書き込む

        data = {
            "氏名": name,
            "フリガナ": hurigana,
            "敬称": honor,
            "氏名(連名1)": joint_name,
            "郵便番号1": postal_code,
            "都道府県1": prefecture,
            "市区町村1": city,
            "地名番地1": street_no,
            "ビル名1" : building
        }
        new_data.append(data)

    # DataFrameに変換
    new_df = pd.DataFrame(new_data)

    # 既存のDataFrameと新しいDataFrameを結合
    output_df = pd.concat([output_df, new_df], ignore_index=True)

    # CSVファイルに書き込む
    output_df.to_csv(output_file, index=False, encoding="shift-jis")


if __name__ == "__main__":
    main()