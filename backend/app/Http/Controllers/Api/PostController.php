<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\JsonResponse | mixed
     */
    public function index()
    {
        $posts = Post::select(['id', 'title', 'slug', 'description', 'created_at', 'updated_at'])->with(['user:name', 'category:name', 'tags:name'])
                      ->paginate(10);

        return response()->json($posts);
    }

    /**
     * Store a newly created resource in storage.
     *
     * @return void
     */
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @return \App\Models\Post
     */
    public function show(string $id)
    {
        return Post::findOrFail($id);
    }

    /**
     * Update the specified resource in storage.
     *
     * @return void
     */
    public function update(Request $request, string $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @return void
     */
    public function destroy(string $id)
    {
        //
    }
}
