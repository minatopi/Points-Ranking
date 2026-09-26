import os
import json
import psycopg


DATABASE_URL = os.environ["DATABASE_URL"]

EXCLUDE_IDS = {
    "b2d3032f-b29e-42d9-a835-2b3c3289669f"
}

OUTPUT_FILE = "ranking.json"


def get_ranking():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT
                    id,
                    username,
                    points
                FROM users
                ORDER BY points DESC NULLS LAST
                LIMIT 11
            """)

            rows = cur.fetchall()

    ranking = []

    for user_id, username, points in rows:

        user_id = str(user_id)

        # 除外ユーザー
        if user_id in EXCLUDE_IDS:
            continue

        ranking.append({
            "rank": len(ranking) + 1,
            "id": user_id,
            "username": username,
            "points": points or 0
        })

        # 10人まで
        if len(ranking) >= 10:
            break

    return ranking


def save_json(ranking):
    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            ranking,
            f,
            ensure_ascii=False,
            indent=2
        )

        f.write("\n")


def main():
    print("ランキング取得開始")

    ranking = get_ranking()

    save_json(ranking)

    print(
        f"ランキングを更新しました: {len(ranking)}人"
    )

    for user in ranking:
        print(
            f'{user["rank"]}位 '
            f'{user["username"]} '
            f'{user["points"]} pt'
        )


if __name__ == "__main__":
    main()
