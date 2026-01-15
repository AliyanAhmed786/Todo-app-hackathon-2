# Chatbot Backend Data Model

## 1. Entity Definitions

### 1.1 Conversation Entity
**Table**: `conversations`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier for the conversation |
| user_id | UUID | Foreign Key to `users.id`, Not Null | Reference to the owning user |
| created_at | DateTime | Not Null | Timestamp when conversation was created |
| updated_at | DateTime | Not Null | Timestamp when conversation was last updated |
| metadata | JSON | Nullable | Additional context data for the conversation |

**Relationships**:
- Belongs to: User (many-to-one)
- Has many: Messages (one-to-many)

### 1.2 Message Entity
**Table**: `messages`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier for the message |
| conversation_id | UUID | Foreign Key to `conversations.id`, Not Null | Reference to the parent conversation |
| sender | String | Not Null, Check: 'user' or 'agent' | Indicates who sent the message |
| content | Text | Not Null | The actual message content |
| timestamp | DateTime | Not Null | When the message was created |
| metadata | JSON | Nullable | Additional context data for AI processing |

**Relationships**:
- Belongs to: Conversation (many-to-one)
- Belongs to: User (through conversation)

## 2. Validation Rules

### 2.1 Conversation Validation
- `user_id` must reference an existing user
- `created_at` must be in the past or present
- `updated_at` must be >= `created_at`
- `metadata` must be valid JSON if provided

### 2.2 Message Validation
- `conversation_id` must reference an existing conversation
- `sender` must be either 'user' or 'agent'
- `content` must not be empty
- `timestamp` must be in the past or present
- `metadata` must be valid JSON if provided

## 3. Indexes

### 3.1 Conversation Indexes
- Primary: `id` (UUID)
- Foreign: `user_id` (to optimize user conversation queries)
- Temporal: `created_at` (to optimize chronological queries)

### 3.2 Message Indexes
- Primary: `id` (UUID)
- Foreign: `conversation_id` (to optimize conversation message queries)
- Temporal: `timestamp` (to optimize chronological message queries)

## 4. State Transitions

### 4.1 Conversation State
- **Active**: New conversation created, ready to receive messages
- **Inactive**: Conversation has no activity for extended period
- **Archived**: Conversation moved to archive after user request or retention policy

*Note: Conversations are implicitly managed - no explicit state field needed*

### 4.2 Message State
- **Pending**: Message received but not yet processed by AI agent
- **Processed**: Message processed and response generated
- **Confirmed**: User acknowledged AI response

*Note: Messages are implicitly managed - no explicit state field needed*

## 5. Relationship Constraints

### 5.1 Referential Integrity
- `conversations.user_id` → `users.id` (CASCADE DELETE: delete conversations when user deleted)
- `messages.conversation_id` → `conversations.id` (CASCADE DELETE: delete messages when conversation deleted)

### 5.2 Data Consistency
- All messages in a conversation belong to the same user (via conversation)
- Timestamps maintain chronological consistency within conversations

## 6. Performance Considerations

### 6.1 Query Patterns
- Most common: Retrieve all messages for a specific conversation
- Secondary: Retrieve all conversations for a specific user
- Occasional: Search messages by content within user's conversations

### 6.2 Size Estimates
- Average conversation: 5-15 messages
- Large conversation: Up to 100 messages
- Message content: Average 50-200 characters, max 1000 characters

## 7. Migration Strategy

### 7.1 Schema Creation
1. Create `conversations` table with indexes
2. Create `messages` table with indexes
3. Establish foreign key relationships
4. Verify referential integrity

### 7.2 Data Migration
- No migration needed - new tables only
- Future: Import historical chat data if required

## 8. Security Considerations

### 8.1 Data Isolation
- User data access restricted by `user_id` foreign key
- Conversation access controlled through authentication
- Message content not exposed to unauthorized users

### 8.2 Privacy
- Message content encrypted at rest if required
- Metadata fields sanitized to prevent information leakage
- No personally identifiable information stored unnecessarily