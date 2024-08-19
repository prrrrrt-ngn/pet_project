function changeQuantity(id, delta) {
    var input = document.getElementById(id);
    var currentValue = parseInt(input.value) || 0;
    var newValue = currentValue + delta;
    if (newValue < 0) newValue = 0; // Не позволяем отрицательные значения
    input.value = newValue;
}