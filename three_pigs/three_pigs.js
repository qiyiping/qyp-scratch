class ThreePigs {
  constructor() {
    this.templates = [
      [ [[-1,0],[0,1]], [[0,-1],[1,0]], [[1,0],[0,-1]], [[0,1],[-1,0]] ],
      [ [[0,1,0]], [[0],[1],[0]] ],
      [ [[-1,-1,0],[0,0,1]], [[0,-1],[0,-1],[1,0]], [[1,0,0],[0,-1,-1]], [[0,1], [-1,0], [-1, 0]]],
    ];
    this.arrangements = [];
    this._cal_all_arrangements();
  }

  _cal_all_arrangements() {
    var b = [ [-1,0,0,-1], [0,0,0,0], [0,0,0,0], [0,0,0,-1] ];
    this._search(b, 0, []);
  }

  _search(b, step, trace) {
    for (let p of this.templates[step]) {
      var matches = this._match(b, p);
      for (let m of matches) {
        var new_b = this._apply(b, p, m);
        var new_trace = [...trace];
        new_trace.push([p,m]);
        if (step == 2) {
          this.arrangements.push([new_trace, new_b]);
        } else {
          this._search(new_b, step+1, new_trace);
        }
      }
    }
  }

  _deepcopy(o) {
    return JSON.parse(JSON.stringify(o));
  }

  _apply(b, p, m) {
    var h = p.length;
    var w = p[0].length;
    var i = m[0];
    var j = m[1];
    var new_b = this._deepcopy(b);
    for (let di = 0; di < h; di++) {
      for (let dj = 0; dj < w; dj++) {
        if (p[di][dj] == 0) {
          new_b[i+di][j+dj] = 1;
        }
        if (p[di][dj] == 1) {
          new_b[i+di][j+dj] = 2;
        }
      }
    }
    return new_b;
  }

  _match(b, p) {
    var matches = [];
    var h = p.length;
    var w = p[0].length;
    for (let i = 0; i < 5-h; i++) {
      for (let j = 0; j < 5-w; j++) {
        var matched = true;
        for (let di = 0; di < h; di++) {
          for (let dj = 0; dj < w; dj++) {
            if (p[di][dj] != -1 && b[i+di][j+dj] != 0) {
              matched = false;
            }
          }
        }

        if (matched) {
          matches.push([i, j]);
        }
      }
    }
    return matches;
  }
}

module.exports = {
  ThreePigs
}
