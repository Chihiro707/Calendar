//今日の日付を取得
const today = new Date();

let year = today.getFullYear();
let month = today.getMonth();

if(selectedDate !== ''){

    const newDate = new Date(selectedDate);
    year = newDate.getFullYear();
    month = newDate.getMonth();
}

//カレンダー作成関数
function createCalendar () {

    //月のタイトルを表示
    document.getElementById("month").textContent = year + "年" + (month + 1) + "月";

    //その月の1日の曜日
    const firstDay = new Date(year, month, 1).getDay();

    //その月の日数
    const lastDate = new Date(year, month + 1, 0).getDate();

    //カレンダーの作成
    const calendar = document.getElementById("calendar");
    calendar.innerHTML = "";
    let row = document.createElement("tr");

    //1日より前の空白
    for (let i = 0; i < firstDay; i++) {
        const cell = document.createElement("td");
        row.appendChild(cell);
    }

    //日付を追加
    for (let day = 1; day <= lastDate; day++) {
        const cell = document.createElement("td");
        cell.textContent = day;
        cell.addEventListener("click", function () {

            const date =
                year + "-" +
                String(month + 1).padStart(2, "0") + "-" +
                String(day).padStart(2, "0");

            window.location.href = "/?date=" + date;
        });
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
}

createCalendar();

//翌月のカレンダーを表示
const nextButton = document.getElementById("next-month");
nextButton.addEventListener("click", function () {

    month++;

    if(month > 11){
        month = 0;
        year++;
    }

    createCalendar();
})

//先月のカレンダーを表示
const previousButton = document.getElementById("previous-month");
previousButton.addEventListener("click", function () {

    month--;

    if(month < 0){
        month = 11;
        year--;
    }

    createCalendar();
})

//予定の削除機能の追加
const deleteEventButtons = document.querySelectorAll(".delete-event");
deleteEventButtons.forEach(function(button) {
    button.addEventListener("click", function () {
        if(confirm("「" + button.dataset.eventTitle + "」の予定を本当に削除しますか？")){
            window.location.href = "/delete_event?id=" + button.dataset.eventId;
        }
    })
})

