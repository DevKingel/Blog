<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/**
 * @mixin IdeHelperComment
 */
class Comment extends Model
{
    use HasFactory;

    public function posts(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
