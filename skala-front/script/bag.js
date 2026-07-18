function showMyBag() {
    var myBag = [
        { name: "지갑", count: 1 },
        { name: "휴대폰", count: 1 },
        { name: "이어폰", count: 1 },
        { name: "노트북", count: 1 },
        { name: "볼펜", count: 3 }
    ];

    var result = "내 가방 속 물품 목록\n\n";

    for (var i = 0; i < myBag.length; i++) {
        result += myBag[i].name + " : " + myBag[i].count + "개\n";
    }

    alert(result);
}