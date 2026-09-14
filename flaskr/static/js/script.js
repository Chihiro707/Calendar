//今日の日付を取得
const today = new Date();
const year = today.getFullYear();
const month = today.getMonth();

//月のタイトルを表示
document.getElementById("month").textContent = year + "年" + (month + 1) + "月";

//その月の1日の曜日
const firstDay = new Date(year, month, 1).getDay();

//その月の日数
const lastDate = new Date(year, month + 1, 0).getDate();

//カレンダーの作成
const calendar = document.getElementById("calendar");
let row = document.createElement("tr");

//1日より前の空白
for (let i = 0; i < firstDay; i++) {
    const cell = document.createElement("td");
    row.appendChild(cell);
}

const schedule = document.getElementById("schedule");
//日付を追加
for (let day = 1; day <= lastDate; day++) {
    const cell = document.createElement("td");
    cell.textContent = day;
    cell.addEventListener("click", function () {

        const date =
            year + "-" +
            String(month + 1).padStart(2, "0") + "-" +
            String(day).padStart(2, "0");

        window.location.href = "/events?date=" + date;
    })
    row.appendChild(cell);

    //土曜日まで来たら次の行へ
    if ((firstDay + day) % 7 === 0) {
        calendar.appendChild(row);
        row = document.createElement("tr");
    }
}

//最後の行を追加
if (row.children.length > 0) {
    calendar.appendChild(row);
}

const edit = document.getElementById("edit");