export default {
  name: 'ctk-tooltip',
  install(Vue) {
    Vue.directive('tooltip', {
      bind(el, binding) {
        el.addEventListener('mouseenter', () => {
          const tooltip = document.createElement('div');
          const tooltipDimension = el.getBoundingClientRect();
          tooltip.setAttribute('class', 'v-tooltip');
          tooltip.setAttribute('id', 'v-tooltip');
          tooltip.innerHTML = binding.value;
          tooltip.style.left = `${tooltipDimension.left + (tooltipDimension.width / 2)}px`;
          tooltip.style.top = `${window.scrollY + tooltipDimension.top + 22}px`;
          document.body.appendChild(tooltip);
        });
        el.addEventListener('mouseleave', () => {
          const elemToRemove = document.getElementById('v-tooltip');
          elemToRemove.parentNode.removeChild(elemToRemove);
        });
      },
    });
  },
};
