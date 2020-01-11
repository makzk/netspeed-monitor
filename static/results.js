(function(){
  let app = new Vue({
    el: '#app',
    data: {
      results: []
    },
    mounted: function () {
      axios.get('/api/results').then(function(data) {
        app.results = data.data;
      });
    }
  });
})();