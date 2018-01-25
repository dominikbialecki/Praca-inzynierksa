from flask import Flask, render_template, redirect, url_for, request
from beets.library import Library
import python.beetsCommands as beetsCommands
import python.dictionary as dictionary
from formencode import variabledecode



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

    return render_template('expandeddetails.html', details=details, dictionary=dict)

@app.route('/edit-data', methods = ['GET', 'POST'])
def edit_data():
    if request.method == 'POST':
        postvars = variabledecode.variable_decode(request.form, dict_char='_')
        albums_id = []
        items_id = []
        for k in range(0, len(postvars), (len(dict.album_keys)+len(dict.item_keys))):
            albums_id.append(postvars.get(str(k)))
            items_id.append(postvars.get(str(k+len(dict.album_keys))))
        print(albums_id)
        print(items_id)
        """
        for singledata in data:
            track = lib.get_item(singledata[0])
            if track!=0:
                track.title = singledata[1]
                track.author = singledata[2]
                track.album = singledata[3]
                track.year = singledata[4]
                album = lib.get_album(track)
                print(track.try_write())
                #track.move(basedir=bytes(path, 'utf-8'))
            tracks.append(track)
        if logs == 1: print('zaktualizowano dane\n')
        """
        return render_template('expandeddetails.html')

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
    dict = dictionary.dictionary(dictionary.english)
    app.run(debug=True, use_reloader=True)
