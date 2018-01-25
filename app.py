from flask import Flask, render_template, redirect, url_for, request
from beets.library import Library
import python.beetsCommands as beetsCommands
import python.dictionary as dictionary

app = Flask(__name__)


@app.route("/")
def main():
    return redirect(url_for('albumy'))


@app.route('/details')
def details():
    dict = dictionary.dictionary(dictionary.polish)
    albums_id = request.args.getlist('id',type=int)
    albums = []
    for album_id in albums_id:
        albums.append(lib.get_album(album_id))
    details = beetsCommands.pack_albums_items(albums)

    return render_template('expandeddetails.html', details=details, dictionary=dict)

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


        beetsCommands.get_covers(lib)
        return redirect('/albums')

@app.route("/albums")
def albumy():
    albums = lib.albums()
    for album in albums:
        album.load()
    alb_sort_album = beetsCommands.pack_albums(sorted(albums, key=lambda x: x.album))
    alb_sort_artist = beetsCommands.pack_albums(sorted(albums, key=lambda x: x.albumartist))
    alb_sort_year = beetsCommands.pack_albums(sorted(albums, key=lambda x: x.year))


    return render_template('albums.html',albums=alb_sort_album, artists=alb_sort_artist, years=alb_sort_year)

@app.route("/artists")
def artysci():
    return render_template('artists.html')

@app.route("/songs")
def muzyka():
    return render_template('songs.html')




if __name__ == "__main__":

    lib = Library(beetsCommands.getLibPath())
    beetsCommands.get_covers(lib)
    app.run(debug=True, use_reloader=True)
