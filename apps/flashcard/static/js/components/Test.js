export default await {
  data() {
    return {
      count: 0
    }
  },
  template: (await axios.get('./js/components/Test-template.html')).data
}