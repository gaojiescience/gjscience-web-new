const throttle = function (func, delay) {
  let timer = null;
  return function () {
    const context = this;
    let args = arguments;
    if (!timer) {
      timer = setTimeout(function () {
        func.apply(context, args);
        timer = null;
      }, delay);
    }
  }
}

export {
  throttle
}
