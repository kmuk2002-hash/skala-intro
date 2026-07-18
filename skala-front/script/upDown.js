function startGame() {
    var computerNum = Math.floor(Math.random() * 50) + 1;
    var count = 0;
    var userNum;

    while (true) {
        var input = prompt("1부터 50 사이의 숫자를 맞춰보세요.");

        if (input === null) {
            alert("게임을 종료합니다.");
            return;
        }

        userNum = Number(input);
        count++;

        if (isNaN(userNum) || input.trim() === "") {
            alert("숫자를 입력해주세요.");
            count--;
            continue;
        }

        if (userNum > computerNum) {
            alert("Down!");
        } else if (userNum < computerNum) {
            alert("Up!");
        } else {
            alert("축하합니다! " + count + "번 만에 맞추셨습니다.");
            break;
        }
    }
}