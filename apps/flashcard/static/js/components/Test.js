export default await {
  data() {
    return {
      count: 0
    }
  },
  template: (await axios.get('./js/components/test-template.html')).data
}