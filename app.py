from flask import Flask, render_template, redirect, url_for, request
from beets.library import Library
import python.beetsCommands as beetsCommands
#from operator import itemgetter


app = Flask(__name__)


@app.route("/")
def main():
    return redirect(url_for('albumy'))


@app.route('/details')
def details():
    albums_id = request.args.getlist('id',type=int)
    albums = []
    for album_id in albums_id:
        albums.append(lib.get_album(album_id))
    details = beetsCommands.pack_albums_items(albums)

    return render_template('details.html', details=details)

@app.route('/edit-data')
def edit_data():

    return render_template('albums.html')

@app.route("/import")
def get_import_path():
    return render_template('import.html')


@app.route('/startImporting', methods=['POST'])
def startImporting():
    if request.method == 'POST':
        path = request.form['Path']
        albums_id = beetsCommands.beetImport(path)
        for album_id in albums_id:
            album = lib.get_album(album_id)
            for item in album.items():
                item.comments = 'unedited'
                item.write()
            album.store()
            album.load()


        beetsCommands.correctPaths(lib)
        return redirect('/albums')

@app.route("/albums")
def albumy():
    albums = lib.albums()
    for album in albums:
        album.load()
    alb_sort_album = beetsCommands.pack_albums(sorted(albums, key=lambda x: x.album))
    alb_sort_artist = beetsCommands.pack_albums(sorted(albums, key=lambda x: x.albumartist))
    alb_sort_year = beetsCommands.pack_albums(sorted(albums, key=lambda x: x.year))
    for album in alb_sort_album:
        print(album[1])

    return render_template('albums.html',albums=alb_sort_album, artists=alb_sort_artist, years=alb_sort_year)

@app.route("/artists")
def artysci():
    return render_template('artists.html')

@app.route("/songs")
def muzyka():
    return render_template('songs.html')




if __name__ == "__main__":

    lib = Library(beetsCommands.getLibPath())
    beetsCommands.correctPaths(lib)
    app.run(debug=True, use_reloader=True)
