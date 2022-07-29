package main

import (
	"context"
	"log"

	"cloud.google.com/go/firestore"
)

type firestoreDB struct {
	client     *firestore.Client
	collection string
}

func newFirestoreDB() *firestoreDB {
	ctx := context.Background()

	client, err := firestore.NewClient(ctx, "getting-started-337714")
	if err != nil {
		log.Fatalf("firestore.NewClient: %v", err)
	}

	return &firestoreDB{
		client:     client,
		collection: "Pets",
	}
}

func (db *firestoreDB) list(ctx context.Context) ([]*Pet, error) {
	docs, err := db.client.Collection(db.collection).Documents(ctx).GetAll()
	if err != nil {
		return nil, err
	}

	pets := make([]*Pet, 0)
	for _, doc := range docs {
		p := &Pet{}
		doc.DataTo(p)
		pets = append(pets, p)
	}

	return pets, nil
}

func (db *firestoreDB) add(ctx context.Context, p *Pet) error {
	ref := db.client.Collection(db.collection).NewDoc()

	p.ID = ref.ID
	if _, err := ref.Create(ctx, p); err != nil {
		return err
	}

	return nil
}

func (db *firestoreDB) get(ctx context.Context, id string) (*Pet, error) {
	ref := db.client.Collection(db.collection).Doc(id)

	docsnap, err := ref.Get(ctx)
	if err != nil {
		return nil, err
	}

	p := &Pet{}
	docsnap.DataTo(p)

	return p, nil
}

func (db *firestoreDB) edit(ctx context.Context, p *Pet) error {
	ref := db.client.Collection(db.collection).Doc(p.ID)

	if _, err := ref.Set(ctx, p); err != nil {
		return err
	}

	return nil
}
