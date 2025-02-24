<?php

use App\Http\Controllers\Api\PostController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

// Route::get('/user', function (Request $request) {
//     return $request->user();
// })->middleware('auth:sanctum');

Route::prefix('/user')->name('user.')->group(function () {
    Route::get('/', [PostController::class, 'index'])->middleware('auth:sanctum')->name('all');

    Route::get('/{id}', [PostController::class, 'show'])->middleware('auth:sanctum')->name('one');

    Route::post('/add', [PostController::class, 'store'])->middleware('auth:sanctum')->name('add');

    Route::delete('/delete/{id}', [PostController::class, 'delete'])->middleware('auth:sanctum')->name('delete');

    Route::patch('/update/{id}', [PostController::class, 'update'])->middleware('auth:sanctum')->name('update');
});

Route::prefix('/posts')->name('post.')->group(function () {
    Route::get('/', [PostController::class, 'index'])->name('all');

    Route::get('/{slug}-{id}', [PostController::class, 'show'])->name('one');

    Route::post('/add', [PostController::class, 'store'])->middleware('auth:sanctum')->name('add');

    Route::delete('/delete/{slug}-{id}', [PostController::class, 'delete'])->middleware('auth:sanctum')->name('delete');

    Route::patch('/update/{slug}-{id}', [PostController::class, 'update'])->middleware('auth:sanctum')->name('update');
});

Route::prefix('/tags')->name('tag.')->group(function () {
    Route::get('/', [PostController::class, 'index'])->name('all');

    Route::get('/{slug}-{id}', [PostController::class, 'show'])->name('one');

    Route::post('/add', [PostController::class, 'store'])->middleware('auth:sanctum')->name('add');

    Route::delete('/delete/{slug}-{id}', [PostController::class, 'delete'])->middleware('auth:sanctum')->name('delete');

    Route::patch('/update/{slug}-{id}', [PostController::class, 'update'])->middleware('auth:sanctum')->name('update');
});

Route::prefix('/comments')->name('comment.')->group(function () {
    Route::get('/', [PostController::class, 'index'])->name('all');

    Route::get('/{id}', [PostController::class, 'show'])->name('one');

    Route::post('/add', [PostController::class, 'store'])->middleware('auth:sanctum')->name('add');

    Route::delete('/delete/{id}', [PostController::class, 'delete'])->middleware('auth:sanctum')->name('delete');

    Route::patch('/update/{id}', [PostController::class, 'update'])->middleware('auth:sanctum')->name('update');
});

Route::prefix('/categories')->name('catagory.')->group(function () {
    Route::get('/', [PostController::class, 'index'])->name('all');

    Route::get('/{slug}-{id}', [PostController::class, 'show'])->name('one');

    Route::post('/add', [PostController::class, 'store'])->middleware('auth:sanctum')->name('add');

    Route::delete('/delete/{slug}-{id}', [PostController::class, 'delete'])->middleware('auth:sanctum')->name('delete');

    Route::patch('/update/{slug}-{id}', [PostController::class, 'update'])->middleware('auth:sanctum')->name('update');
});
