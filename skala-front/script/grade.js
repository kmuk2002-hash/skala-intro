function calculateGrade() {
    var subjects = ["HTML", "CSS", "JavaScript"];
    var total = 0;
    var score;

    for (var i = 0; i < subjects.length; i++) {
        score = Number(prompt(subjects[i] + " 점수를 입력하세요."));
        total += score;
    }

    var average = total / subjects.length;
    var result = average >= 60 ? "합격" : "불합격";
    var grade;

    if (average >= 90) {
        grade = "A";
    } else if (average >= 80) {
        grade = "B";
    } else if (average >= 70) {
        grade = "C";
    } else if (average >= 60) {
        grade = "D";
    } else {
        grade = "F";
    }

    alert("총점: " + total + "점, 평균: " + average + ", 등급: " + grade + ", 결과: " + result + "입니다!");
}