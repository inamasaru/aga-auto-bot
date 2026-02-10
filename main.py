import os,random,requests,anthropic,base64

# キーワードリスト（20個に拡張）
KW=[
    ("AGA 20代 M字","【20代】AGA治療費用と対策"),
    ("AGA オンライン 安い","安いオンラインAGA診療比較"),
    ("フィナステリド 副作用","フィナステリド副作用と対処法"),
    ("ミノキシジル 効果","ミノキシジルの効果と期間"),
    ("AGA 初期脱毛 いつまで","AGA初期脱毛の期間と対処法"),
    ("薄毛 バレない 治療","バレないAGA治療方法"),
    ("AGA 費用 月額","AGA治療の月額費用相場"),
    ("デュタステリド 違い","デュタステリドとフィナステリドの違い"),
    ("AGA 遺伝 確率","AGAの遺伝確率と対策"),
    ("AGA 効果なし 原因","AGA治療で効果が出ない原因"),
    ("AGA 30代 おすすめ","30代におすすめのAGA治療"),
    ("AGA 女性 FAGA","女性のAGA（FAGA）治療"),
    ("AGA 治療 後悔","AGA治療で後悔しないために"),
    ("AGA やめたら","AGA治療をやめたらどうなる"),
    ("プロペシア ジェネリック","プロペシアとジェネリックの違い"),
    ("AGA 保険適用","AGA治療は保険適用される？"),
    ("薄毛 シャンプー 効果","薄毛対策シャンプーの効果"),
    ("AGA 食事 栄養","AGA対策に効果的な食事と栄養"),
    ("ミノタブ 副作用","ミノキシジルタブレットの副作用"),
    ("AGA 進行 止める","AGA進行を止める方法")
]

# アフィリエイトリンク（A8.net承認済みプログラム）
# 薬用グローリン・ギガ（発毛促進剤）- 2026/01/28承認
AFFILIATE_LINKS = """
<div class="clinic-comparison">
<h3>おすすめAGA対策商品</h3>
<ul>
<li><strong>薬用グローリン・ギガ</strong> - 販売実績260万本！リピート率93%の発毛促進剤<br>
<a href="https://px.a8.net/svt/ejp?a8mat=4AVGK2+7QMVW2+3NZO+1NJK7M" target="_blank" rel="nofollow">820円から始める発毛促進応援キャンペーン</a></li>
</ul>
<p>※他のAGAクリニックプログラムは現在申請中です。承認され次第追加予定。</p>
</div>
"""

def main():
    k=random.choice(KW)
    # プロンプトにアフィリエイトリンクを含める指示を追加
    prompt = f"""AGA専門ライターとして「{k[1]}」(KW:{k[0]})で3500文字のSEO記事をHTML形式で書いて。

構成:
1. 導入（悩みの共感）
2. 問題提起（AGAの原因と進行）
3. 解決策（治療法の紹介）
4. クリニック比較（以下のHTMLをそのまま挿入）
{AFFILIATE_LINKS}
5. FAQ（よくある質問3つ）
6. まとめ（行動を促す）

注意: クリニック比較セクションには上記のHTMLをそのまま使用してください。"""

    c=anthropic.Anthropic(api_key=os.environ["CLAUDE_API_KEY"]).messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=6000,
        messages=[{"role":"user","content":prompt}]
    ).content[0].text
    
    cred=base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
    r=requests.post(
        f"{os.environ['WP_URL']}/index.php?rest_route=/wp/v2/posts",
        json={"title":k[1],"content":c,"status":"draft"},
        headers={"Authorization":f"Basic {cred}","Content-Type":"application/json"}
    )
    print("OK" if r.status_code==201 else r.text)

if __name__=="__main__":
    main()
