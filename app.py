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
        albums_newdata = []
        items_newdata = []
        items_id_grouped = []       #used to help count number of items
        album_keys_number = len(dict.album_keys)
        item_keys_number = len(dict.item_keys)
        print(len(postvars))

        while (len(albums_id)*(album_keys_number+len(items_id_grouped)*item_keys_number)) != len(postvars):
            albums_number = len(albums_id)

            album_keys_number = len(dict.album_keys)
            item_keys_number = len(dict.item_keys)
            album_len = albums_number * (album_keys_number + len(items_id) * item_keys_number)

            album_newdata = []
            for k in range(0, album_keys_number):
                album_newdata.append(postvars.get(str(albums_number * album_len +k)))
            albums_newdata.append(album_newdata)
            albums_id.append(int(album_newdata[-1]))
            album = lib.get_album(albums_id[-1])

            album_items_id = []
            for item in album.items():
                album_items_id.append(item.id)
                items_id_grouped.append(item.id)
            items_id.append(album_items_id)

            for k in range(0, len(album_items_id)):
                item_newdata = []
                for j in range(0, item_keys_number):
                    item_newdata.append(postvars.get(str(albums_number * (album_keys_number + len(album_items_id) * item_keys_number) + album_keys_number + k * item_keys_number + j)))
                items_newdata.append(item_newdata)


        return redirect('/albums')
        #return render_template('expandeddetails.html')

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
    alb_sort_album = beetsCommands.pack_albums_items(sorted(albums, key=lambda x: x.album))
    alb_sort_artist = beetsCommands.pack_albums_items(sorted(albums, key=lambda x: x.albumartist))
    alb_sort_year = beetsCommands.pack_albums_items(sorted(albums, key=lambda x: x.year))


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
