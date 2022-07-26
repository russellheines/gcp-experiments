package main

import (
	"testing"
)

func TestAdd(t *testing.T) {

	memoryDB := newMemoryDB()
	memoryDB.add(&Pet{Name: "Tom", Type: "Fish"})

	if len(memoryDB.list()) != 1 {
		t.Error("expected one pet")
	}
}

func TestGet(t *testing.T) {

	memoryDB := newMemoryDB()
	memoryDB.add(&Pet{Name: "Tom", Type: "Fish"})

	if p, _ := memoryDB.get("1"); p.Name != "Tom" {
		t.Error("expected \"Tom\"")
	}

	if _, err := memoryDB.get("2"); err == nil {
		t.Error("expected \"pet not found\"")
	}
}

func TestEdit(t *testing.T) {

	memoryDB := newMemoryDB()
	memoryDB.add(&Pet{Name: "Tom", Type: "Fish"})
	memoryDB.edit(&Pet{ID: "1", Name: "Flippy Twitch", Type: "Fish"})

	if p, _ := memoryDB.get("1"); p.Name != "Flippy Twitch" {
		t.Error("expected \"Flippy Twitch\"")
	}

	if err := memoryDB.edit(&Pet{Name: "Flippy Twitch", Type: "Fish"}); err == nil {
		t.Error("expected \"missing pet id\"")
	}
}

func TestDelete(t *testing.T) {

	memoryDB := newMemoryDB()
	memoryDB.add(&Pet{Name: "Tom", Type: "Fish"})
	memoryDB.delete("1")

	if len(memoryDB.list()) != 0 {
		t.Error("expected no pets")
	}

	if err := memoryDB.delete("1"); err == nil {
		t.Error("expected: \"pet not found\"")
	}

}
