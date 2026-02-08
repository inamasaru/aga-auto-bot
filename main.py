import os,random,requests,anthropic,base64
KW=[("AGA 20代 M字","【20代】AGA治療費用と対策"),("AGA オンライン 安い","安いオンラインAGA診療比較"),("フィナステリド 副作用","フィナステリド副作用と対処法"),("ミノキシジル 効果","ミノキシジルの効果と期間")]
def main():
    k=random.choice(KW)
    c=anthropic.Anthropic(api_key=os.environ["CLAUDE_API_KEY"]).messages.create(model="claude-sonnet-4-20250514",max_tokens=6000,messages=[{"role":"user","content":f"AGA専門ライターとして「{k[1]}」(KW:{k[0]})で3500文字のSEO記事をHTML形式で書いて。導入→問題→解決策→クリニック比較→FAQ→まとめの構成で。"}]).content[0].text
    cred=base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
    r=requests.post(f"{os.environ['WP_URL']}/index.php?rest_route=/wp/v2/posts",json={"title":k[1],"content":c,"status":"draft"},headers={"Authorization":f"Basic {cred}","Content-Type":"application/json"})
    print("OK" if r.status_code==201 else r.text)
if __name__=="__main__":main()
