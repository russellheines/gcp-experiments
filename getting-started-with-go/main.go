package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"net/http"
	"path"

	"cloud.google.com/go/storage"
	"github.com/gofrs/uuid"
)

type PetClinic struct {
	db PetDatabase

	bktName string
	bkt     *storage.BucketHandle
}

type Pet struct {
	ID       string
	Name     string
	Type     string
	ImageURL string
}

type PetDatabase interface {
	list(ctx context.Context) ([]*Pet, error)
	//ListBooks(context.Context) ([]*Book, error)

	get(ctx context.Context, id string) (*Pet, error)
	//GetBook(ctx context.Context, id string) (*Book, error)

	add(ctx context.Context, p *Pet) error
	//AddBook(ctx context.Context, b *Book) (id string, err error)

	//DeleteBook(ctx context.Context, id string) error

	edit(ctx context.Context, p *Pet) error
	//UpdateBook(ctx context.Context, b *Book) error
}

func (pc *PetClinic) uploadFileFromForm(r *http.Request) (string, error) {

	f, fh, err := r.FormFile("image")
	if err != nil {
		if err == http.ErrMissingFile {
			return r.FormValue("imageURL"), nil
		} else {
			return "", err
		}
	}

	// random filename, retaining existing extension.
	name := uuid.Must(uuid.NewV4()).String() + path.Ext(fh.Filename)

	w := pc.bkt.Object(name).NewWriter(r.Context())

	if _, err := io.Copy(w, f); err != nil {
		return "", err
	}
	if err := w.Close(); err != nil {
		return "", err
	}

	const publicURL = "https://storage.googleapis.com/%s/%s"
	return fmt.Sprintf(publicURL, pc.bktName, name), nil
}

func main() {
	ctx := context.Background()

	client, err := storage.NewClient(ctx)
	if err != nil {
		log.Fatal(err)
	}
	bktName := "getting-started-337714_bucket"
	bkt := client.Bucket(bktName)

	pc := &PetClinic{
		db:      newFirestoreDB(),
		bktName: bktName,
		bkt:     bkt,
	}

	http.HandleFunc("/", pc.listHandler)
	http.HandleFunc("/detail/", pc.detailHandler)
	http.HandleFunc("/add/", pc.addHandler)
	http.HandleFunc("/edit/", pc.editHandler)

	log.Printf("Listening on localhost:8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}
