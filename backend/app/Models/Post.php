<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;

/**
 * @mixin IdeHelperPost
 */
class Post extends Model
{
    /** @use HasFactory<\Database\Factories\UserFactory> */
    use HasFactory;

    protected $fillable = [
        'title',
        'slug',
        'description',
        'content',
        'user_id',
        'category_id',
    ];

    /**
     * @return BelongsTo<\App\Models\User, $this>
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    /**
     * @return BelongsToMany<\App\Models\Tag, $this>
     */
    public function tags()
    {
        return $this->belongsToMany(Tag::class)
            ->select(['tags.id', 'tags.name'])->withPivot([]);
    }

    /**
     * @return belongsTo<\App\Models\Category, $this>
     */
    public function category()
    {
        return $this->belongsTo(Category::class);
    }

    /**
     * @return hasMany<\App\Models\Comment, $this>
     */
    public function comments()
    {
        return $this->hasMany(Comment::class);
    }
}
