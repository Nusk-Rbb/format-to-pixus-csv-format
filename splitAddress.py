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
    output_file = "pixus_new_receivers.csv"
    # CSVファイルを読み込む
    input_df = pd.read_csv(input_file)
    output_df = pd.read_csv(output_file)


    new_data  = []
    input = {
        "name": input_df["氏名"],
        "honor": input_df["敬称"],
        "hurigana": input_df["フリガナ"],
        "joint_name": input_df["氏名(連名１)"],
        "joint_hurigana": input_df["フリガナ(連名1)"],
        "postal": input_df["郵便番号"],
        "address": input_df["住所1"],
        "building": input_df["住所2"],
    }

    # 1.郵便番号と住所から都道府県、市区町村、それ以外を抽出し、
    # 2.CSVファイルに書き込む
    for postal_code, address, building, name, joint_name, joint_name_hurigana, honor, hurigana in zip(
        input["postal"],
        input["address"],
        input["building"],
        input["name"], 
        input["joint_name"], 
        input["joint_hurigana"],
        input["honor"], 
        input["hurigana"]):
        # 郵便番号と住所から都道府県、市区町村、それ以外を抽出
        address_from_postal = get_address_by_postal_code(postal_code)
        prefecture = address_from_postal["results"][0]["address1"]
        city = address_from_postal["results"][0]["address2"]
        street_no = get_street_by_address(prefecture, city, address)

        if(pd.isnull(joint_name)):
            joint_name = ""
            joint_name_hurigana = ""


        if(pd.isnull(building)):
            building = ""

        postal_code = postal_code.replace("-", "")
        name = name.replace("　", " ")
        hurigana = hurigana.replace("　", " ")

        print(name, hurigana, joint_name, joint_name_hurigana, honor, prefecture, city, street_no, building)
        # CSVファイルに書き込む

        data = {
            "氏名": name,
            "フリガナ": hurigana,
            "敬称": honor,
            "氏名(連名1)": joint_name,
            "フリガナ(連名1)" : joint_name_hurigana,
            "敬称(連名1)" : honor,
            "郵便番号1": postal_code,
            "都道府県1": prefecture,
            "市区町村1": city,
            "地名番地1": street_no,
            "ビル名1" : building,
            "分類(住所)1" : "自宅",
            "グループ" : "松治、いつよ",
            "記録1" : "2025,0,0,0,0",
            "記録2" : "2024,0,0,0,0",
            "記録3" : "2023,0,0,0,0",
        }
        new_data.append(data)

    # DataFrameに変換
    new_df = pd.DataFrame(new_data)

    # 既存のDataFrameと新しいDataFrameを結合
    output_df = pd.concat([output_df, new_df], ignore_index=True)

    # CSVファイルに書き込む
    output_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    main()