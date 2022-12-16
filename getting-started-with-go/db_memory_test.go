package main

import (
	"context"
	"testing"
)

func TestAdd(t *testing.T) {

	ctx := context.Background()

	memoryDB := newMemoryDB()
	memoryDB.add(ctx, &Pet{Name: "Tom", Type: "Fish"})

	if pets, err := (memoryDB.list(ctx)); err != nil {
		t.Error(err)
	} else if len(pets) != 1 {
		t.Error("expected one pet")
	}
}

func TestGet(t *testing.T) {

	ctx := context.Background()

	memoryDB := newMemoryDB()
	memoryDB.add(ctx, &Pet{Name: "Tom", Type: "Fish"})

	if p, err := memoryDB.get(ctx, "1"); err != nil {
		t.Error(err)
	} else if p.Name != "Tom" {
		t.Error("expected \"Tom\"")
	}

	if _, err := memoryDB.get(ctx, "2"); err == nil {
		t.Error("expected \"pet not found\"")
	}
}

func TestEdit(t *testing.T) {

	ctx := context.Background()

	memoryDB := newMemoryDB()
	memoryDB.add(ctx, &Pet{Name: "Tom", Type: "Fish"})
	memoryDB.edit(ctx, &Pet{ID: "1", Name: "Flippy Twitch", Type: "Fish"})

	if p, err := memoryDB.get(ctx, "1"); err != nil {
		t.Error(err)
	} else if p.Name != "Flippy Twitch" {
		t.Error("expected \"Flippy Twitch\"")
	}

	if err := memoryDB.edit(ctx, &Pet{Name: "Flippy Twitch", Type: "Fish"}); err == nil {
		t.Error("expected \"missing pet id\"")
	}
}

func TestDelete(t *testing.T) {

	ctx := context.Background()

	memoryDB := newMemoryDB()
	memoryDB.add(ctx, &Pet{Name: "Tom", Type: "Fish"})
	memoryDB.delete("1")

	if pets, err := (memoryDB.list(ctx)); err != nil {
		t.Error(err)
	} else if len(pets) != 0 {
		t.Error("expected no pets")
	}

	if err := memoryDB.delete("1"); err == nil {
		t.Error("expected: \"pet not found\"")
	}
}
