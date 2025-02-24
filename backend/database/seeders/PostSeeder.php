<?php

namespace Database\Seeders;

use App\Models\Category;
use App\Models\Comment;
use App\Models\Post;
use App\Models\Tag;
use Illuminate\Database\Seeder;

class PostSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // Générer 50 catégories
        Category::factory(50)->create();

        // Générer 200 tags
        Tag::factory(200)->create();

        // Générer 3000 posts
        Post::factory(3000)->create()->each(function ($post) {
            // Associer 1 à 3 tags aléatoires
            $tags = Tag::inRandomOrder()->limit(rand(1, 3))->pluck('id');
            $post->tags()->attach($tags);

            // Générer 0 à 5 commentaires par post
            Comment::factory(rand(0, 5))->create(['post_id' => $post->id]);
        });
    }
}
