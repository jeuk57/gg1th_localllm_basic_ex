// textarea에 공백일 경우 경고창 띄우기 (index.html의 Add 버튼에만 존재)
let task = document.getElementById("task");
let add_task = document.getElementById("add_task");
if (task && add_task) {
  add_task.addEventListener("click", (e) => {
    if (task.value == "") {
      alert("입력한 TODO가 없습니다.");
      // submit 방지함
      e.preventDefault();
      return false;
    }
  });
}

// Delete: 페이지 이동 없이 백그라운드로 삭제하고,
// 화면에서는 목록에서 지우지 않고 취소선만 표시함
document.querySelectorAll(".delete-form").forEach((form) => {
  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const button = form.querySelector("button");
    if (button.disabled) {
      // 이미 처리된 항목에 대한 중복 클릭 방지
      return;
    }

    // 응답을 기다리지 않고 먼저 화면부터 취소선 처리 + 버튼 비활성화
    button.disabled = true;
    const taskDiv = form.closest(".task");
    taskDiv.querySelector(".task-text").classList.add("deleted");

    fetch(form.action, { method: "POST" }).catch(() => {
      alert("삭제 요청 전송에 실패했습니다. 새로고침 후 다시 시도해주세요.");
    });
  });
});
